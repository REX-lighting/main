import subprocess
import sys
import os

def add_black_bar(input_file, output_file=None):
    """
    Add a horizontal black bar that takes 1/3 of the screen in the middle of a video.
    
    Args:
        input_file: Path to input video file (mp4, avi, mov, etc.)
        output_file: Path to output video file (optional, defaults to input_file_with_bar.mp4)
    """
    
    # Check if FFmpeg is installed
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except FileNotFoundError:
        print("ERROR: FFmpeg is not installed or not in PATH")
        print("Please install FFmpeg from https://ffmpeg.org/download.html")
        sys.exit(1)
    
    # Generate output filename if not provided
    if output_file is None:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_with_bar{ext}"
    
    # Get video dimensions (width and height)
    probe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        input_file
    ]
    
    try:
        result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        width, height = map(int, result.stdout.strip().split(','))
    except:
        print("ERROR: Could not get video dimensions. Make sure the file is a valid video.")
        sys.exit(1)
    
    # Calculate dimensions
    bar_height = height // 3
    # Add some to the black bar
    bar_height += 80
    top_half = height // 2
    new_height = height + bar_height  # Original height + bar
    
    # FFmpeg command to split video and add black bar
    # 1. Crop top half
    # 2. Crop bottom half  
    # 3. Create black bar with exact dimensions
    # 4. Stack them vertically
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-filter_complex',
        f'[0:v]crop=iw:{top_half}:0:0[top];'
        f'[0:v]crop=iw:{height - top_half}:0:{top_half}[bottom];'
        f'color=black:s={width}x{bar_height}:d=1[bar];'
        f'[top][bar][bottom]vstack=inputs=3[out]',
        '-map', '[out]',
        '-map', '0:a?',  # Copy audio if exists
        '-c:a', 'copy',  # Copy audio without re-encoding
        '-y',  # Overwrite output file if exists
        output_file
    ]
    
    print(f"Processing: {input_file}")
    print(f"Output: {output_file}")
    print(f"Splitting video and inserting {bar_height}px black bar in the middle")
    print(f"Original dimensions: {width}x{height}")
    print(f"New dimensions: {width}x{new_height}")
    
    # Run FFmpeg
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"\nSuccess! Output saved to: {output_file}")
    except subprocess.CalledProcessError:
        print("\nERROR: FFmpeg processing failed")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_video> [output_video]")
        print("Example: python script.py input.mp4")
        print("Example: python script.py input.mp4 output.mp4")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"ERROR: File '{input_file}' not found")
        sys.exit(1)
    
    add_black_bar(input_file, output_file)
