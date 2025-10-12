import subprocess
import sys
import os

def add_black_bar(input_file, output_file=None, output_resolution=None):
    """
    Add a horizontal black bar that takes 1/3 of the screen in the middle of a video.
    
    Args:
        input_file: Path to input video file (mp4, avi, mov, etc.)
        output_file: Path to output video file (optional, defaults to input_file_with_bar.mp4)
        output_resolution: Tuple of (width, height) for final output resolution (optional)
                          Crops equal amounts from each side to match resolution
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
        'ffprobe', '-v', 'error',
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
    top_half = height // 2
    new_height = height + bar_height  # Original height + bar
    new_width = width
    
    # Build the filter complex string
    filter_parts = []
    
    # Split and add black bar
    filter_parts.append(f'[0:v]crop=iw:{top_half}:0:0[top];')
    filter_parts.append(f'[0:v]crop=iw:{height - top_half}:0:{top_half}[bottom];')
    filter_parts.append(f'color=black:s={width}x{bar_height}:d=1[bar];')
    filter_parts.append(f'[top][bar][bottom]vstack=inputs=3[stacked];')
    
    # Apply cropping if output resolution is specified
    if output_resolution:
        target_width, target_height = output_resolution
        
        # Validate output resolution
        if target_width > new_width or target_height > new_height:
            print(f"ERROR: Output resolution {target_width}x{target_height} is larger than video with bar {new_width}x{new_height}")
            sys.exit(1)
        
        # Calculate crop amounts (equal from each side)
        crop_x = (new_width - target_width) // 2
        crop_y = (new_height - target_height) // 2
        
        filter_parts.append(f'[stacked]crop={target_width}:{target_height}:{crop_x}:{crop_y}[out]')
        
        final_width = target_width
        final_height = target_height
        
        print(f"Cropping {crop_x}px from left/right and {crop_y}px from top/bottom")
    else:
        filter_parts.append(f'[stacked]copy[out]')
        final_width = new_width
        final_height = new_height
    
    filter_complex = ''.join(filter_parts)
    
    # FFmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_file,
        '-filter_complex', filter_complex,
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
    print(f"Dimensions with bar: {new_width}x{new_height}")
    print(f"Final output dimensions: {final_width}x{final_height}")
    
    # Run FFmpeg
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"\nSuccess! Output saved to: {output_file}")
    except subprocess.CalledProcessError:
        print("\nERROR: FFmpeg processing failed")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_video> [output_video] [width] [height]")
        print("Example: python script.py input.mp4")
        print("Example: python script.py input.mp4 output.mp4")
        print("Example: python script.py input.mp4 output.mp4 1920 1080")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Parse optional resolution parameters
    output_resolution = None
    if len(sys.argv) >= 5:
        try:
            output_width = int(sys.argv[3])
            output_height = int(sys.argv[4])
            output_resolution = (output_width, output_height)
        except ValueError:
            print("ERROR: Width and height must be integers")
            sys.exit(1)
    elif len(sys.argv) == 4:
        print("ERROR: Please provide both width and height for output resolution")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"ERROR: File '{input_file}' not found")
        sys.exit(1)
    
    add_black_bar(input_file, output_file, output_resolution)
