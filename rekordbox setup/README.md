1. Check Video Preferences:
	Go to Preferences > Extensions > Video.
	Make sure the Enable Video Function checkbox is ticked (selected).

2. Click the video button that appear in taskbar (see video for more details)

3. Load in track

4. Double click to have it pop out

![Rekordbox gif](videos/how-to-enable-video-rekordbox.gif)

Once this is done you should be able to display videos, but owe noes, rekirdbox is adding a bar across. We will get around this by modifying the video so the bar is ontop of nothing, then modiftying the screen.

To modify your music videos to be outside the bar that recordbox has there is a helper function

```
python3 convert_music.py videos/test_input.mp4
```

It also supports output information after. This will add a gap inbetween your video (this will be removed later)

To display your visuals on a seperate screen I like the virtual display adaptor located [here](https://github.com/VirtualDrivers/Virtual-Display-Driver/releases)

Make sure to have extend display. This is a good [video](https://www.youtube.com/watch?v=jN5YnHlC0fE). It also shows you how to control resolution which is helpful. Use Windows + Shift + Left/Right Arrow to move the window around easily.

Use the broadcast_screen.toe to broadcast to people on your local network. This file also removes the gap added to your video.

Use the ndi_out.tox to capture this for visuals
