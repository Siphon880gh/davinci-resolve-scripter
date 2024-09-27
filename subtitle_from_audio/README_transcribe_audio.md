### Description

This script takes in an audio file and outputs a subtitle file in the SRT format. Your SRT format could be imported as a subtitle track in DaVinci, OR you can have the script generate IG-styled Text+ clips for a more dramatic text.

## Installation

To install the required package, run:

```
pip install openai-whisper torch
```

Make sure ffmpeg is installed on your machine. You can google installation instructions for ffmpeg on your particular OS.

## Usage (Adjustment)

You can choose the model and device to use in the `chosen_processor.py` file.

| Size      | Parameters | English-only | Multilingual |
|-----------|------------|--------------|--------------|
| tiny      | 39 M       | ✓            | ✓            |
| base      | 74 M       | ✓            | ✓            |
| small     | 244 M      | ✓            | ✓            |
| medium    | 769 M      | ✓            | ✓            |
| large     | 1550 M     | x            | ✓            |
| large-v2  | 1550 M     | x            | ✓            |

Then add where the wav or mp3 file with speech is at. Then add where you want to save the SRT file to. For example, adjust in `transcribe_audio/generate.py`:

```
INPUT_AUDIO="eleven_labs.mp3"
OUTPUT_DIR="./" # Eg. ./
OUTPUT_FILENAME_W_EXT="eleven_labs.srt"
```

## Usage

### Generate the SRT file

To transcribe audio into a subtitle SRT file, adjust the `subtitle_from_audio/generate.py` file for the audio wav or mp3 file (you could have generated it from text-to-speech or is an actual audio recording of your narration). You may adjust the srt output path but is not recommended because the title plus generator at `drop_textp.py` if you choose to use it, would have to be adjusted to at its SRT path.

Finally, you may adjust `max_line_count` and `max_line_width`. If you will use the SRT file to create Text+ clips, your width is limited between 30 and 35 unless you change the font and/or font size of the Text+ clip template (to be discussed later). If you will use the traditional subtitle track instead of Text+ track clips generation, you are not really limited on the width.

Generate the SRT with this:
```bash
python generate.py
```

### Option A: Create synced subtitle track

Look for the srt file in the output folder you've set in the script. You can drop this subtitle file (default named `drop_subtitle_media.srt`) into your media pool, then create a Subtitle track in your timeline, then lastly drop the SRT from the media pool into that track.

### Option B: Create Text+ clips on an empty video track

If instead of using a subtitle track, you want to generate Text+ clips across an empty video track so that it can follow IG-styled middle of the screen text. There are two major phases to create this track. 

- First, you need to prep your project so there's a Text+ clip in the media pool whose font settings will be used as a basis to create those Text+ clips into the video traack. Also you need an empty video track. 
- Second, after adjusting `drop_textp.py`, you will need to drop the script into the DaVinci console. 

1. Look into the Effects panel (top left panel), and search for "Text". Drag the "Text+" into any area on a video track. Then drag that "Text+" clip from the video track into the media pool. Now delete the timeline's "Text+" clip. You now have the "Text+" clip in the media pool and no "Text+" clip from this exercise in the timeline. Finally, adjust any font settings at the media pool's Text+ clip because this will be the template used to generate the Text+ subtitle clips into the timeline.

2. Then adjust the drop_textp.py: 
- See if you need to adjust the path to the SRT file
- See if you need to adjust SCRIPT_DIR which is the absolute path to the `drop_textp.py`.
Explanation: This is needed because the free DaVinci Resolve does not expose the script's path when drag and dropping into a console, which is needed for the code
- See if for your current project, you have an empty video track 2. If not, you have to adjust the number at TARGET_EMPTY_VIDEO_TRACK. You are required to have an empty video track for the Text+ clips to insert into from the first frame.
- See if you want to adjust TRANSFORM_EACH_TEXTP if you want uppercasing presets to run on each Text+ clip. Some uppercasing presets include uppercasing the first word of each Text+ clip, or uppercasing all words.

3. Once you are done adjusting `drop_textp.py`, go ahead and drag and drop the script into the DaVinci console. On success, you will see Text+ clips fill the empty video track and those Text+ clips will have the subtitle that sync with the audio.

## Some video editing required

You may find that by chance your subtitle could end or start too soon from another video clip starting or ending. This would be jarring. So adjust the video clips as needed.

![Subtitle should not end or start too soon from another video clip starting or ending](README_subtitle_tip.png)