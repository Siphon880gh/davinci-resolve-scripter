# Init Resolve
# ------------------------------------------------
import importlib.util
resolve = None

import sys
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples')

if resolve == None:
    resolve = None
    if importlib.util.find_spec("DaVinciResolveScript") is not None:
        import DaVinciResolveScript as dvr_script
        test_init = dvr_script.scriptapp("Resolve")
        if(test_init is not None):
            resolve = test_init
        else:
            if app is not None: # type: ignore
                resolve = app.GetResolve() # type: ignore
    else:
        # app is available during runtime with DaVinci Resolve's console
        if app is not None: # type: ignore
            resolve = app.GetResolve() # type: ignore
    globals()['resolve'] = resolve


if resolve is None:
	print("Failed to connect to DaVinci Resolve.")
	exit()
else:
    print("Connected to DaVinci Resolve API...")

# _OTHER IMPORTS
# ------------------------------------------------
import re
import os
from dep_textp_transformers import uppercase_all, uppercase_first_word, uppercase_tagged_text

# Common Objects
# ------------------------------------------------
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_pool = project.GetMediaPool()

# Remove timeline block if not applicable
try: 
    timeline = project.GetCurrentTimeline()
except Exception as e: # Comment/Uncomment as needed
    # print("ERROR - No timeline is currently open.")
    # print(e)
    # exit()
    media_pool.CreateEmptyTimeline("Timeline 1")
    timeline = project.GetCurrentTimeline()
    pass

# Remove this video track 1 block if not applicable
try: 
    track = timeline.GetItemsInTrack('video', 1)
except Exception as e:
    print("ERROR - No video track is available in opened timeline. Does your script work with an existing track? If not, you don't need this object - go ahead and remove this block.")
    print(e)
    exit()

# _SCRIPT:
# ------------------------------------------------

# _ADJUST 1 of 4
SRT_FILENAME = "drop_subtitle_media.srt"


# _ADJUST 2 of 4
# Note you have to write the absolute path to the SRT file
# Why: `os.path.dirname(os.path.abspath(__name__)) would fail because it's a 
# drop in script into DaVinci Resolve console which will change __name__ abs pathing 
# to /Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/..
SCRIPT_DIR = "/Users/wengffung/dev/web/davinci/subtitle_from_audio/"
if not os.path.exists(SCRIPT_DIR):
    SCRIPT_DIR = "/Users/wengffung/dev/web/davinci/05_subtitle_from_audio/"
srt_file_path = os.path.join(SCRIPT_DIR, SRT_FILENAME)
print(f"Reading SRT file from: {srt_file_path}")


# _ADJUST 3 of 4
# Make sure you have an empty video track to insert the Text+ based off subtitles
TARGET_EMPTY_VIDEO_TRACK = 2


# _ADJUST 4 of 4
# Adjust text transformations, if any, to apply to each Text+ clip's text
# Eg. TRANSFORM_EACH_TEXTP = [uppercase_all]
# Eg. TRANSFORM_EACH_TEXTP = [uppercase_first_word]
# Eg. TRANSFORM_EACH_TEXTP = [uppercase_tagged_text] # Eg. <u>Word<u> becomes WORD
# Eg. TRANSFORM_EACH_TEXTP = [uppercase_first_word, uppercase_tagged_text]
# Eg. TRANSFORM_EACH_TEXTP = []
TRANSFORM_EACH_TEXTP = [uppercase_tagged_text]

# Assure is on the Edit page
resolve.OpenPage("edit")

frame_rate = timeline.GetSetting('timelineFrameRate')
frame_rate = float(frame_rate) if frame_rate else 24.0  # Default to 24 FPS if not set
print("\nRetrieved Frame Rate: ", frame_rate)

media_pool_items_list = []

text_plus_template_search_pattern = re.compile(r'text|title|subtitle', re.IGNORECASE)

def init_by_finding_textp_clip_in_media_pool():
    media_pool = project.GetMediaPool()
    folder = media_pool.GetRootFolder()

    recursive_search_on_media_pool(folder, media_pool_items_list, text_plus_template_search_pattern)

def recursive_search_on_media_pool(folder, media_pool_items_list, pattern):
    # Retrieve all clip properties at once.
    items = folder.GetClipList()
    item_properties = [item.GetClipProperty() for item in items]

    # Iterate through item properties to see if they match
    # the search pattern that we've established.
    for item, properties in zip(items, item_properties):
        itemType = properties.get("Type", "")
        item_name = item.GetName()
        clip_name = properties.get("Clip Name", "")

        # Debug statements to track the computation.
        print(f"\nChecking item: {item_name}, Type: {itemType}")

        desired_type = "Fusion Title" # Fusion Title is the type of Text+ in the Media Pool
        if itemType == desired_type:
            # Check if item_name or clip_name contains the search pattern.
            if pattern.search(item_name) or pattern.search(clip_name):
                print(f"Match found: {item_name}")
                media_pool_items_list.append(item)
            else:
                print(f"No match for pattern in item: {item_name}")
        else:
            print(f"Item {item_name} is not of type '{desired_type}'.")

    # Recursively search subfolders in the media pool.
    subfolders = folder.GetSubFolderList()
    for subfolder in subfolders:
        recursive_search_on_media_pool(subfolder, media_pool_items_list, pattern)

init_by_finding_textp_clip_in_media_pool()

# After the function call, print the items found.
print("\nItems matching the pattern:")
for item in media_pool_items_list:
    print(item.GetName())

def generate_text_plus_subtitle_clips(srt_path, video_track_index, frame_rate, transformations=None):
    content = ''
    subs = []
    global media_pool
    
    # Get current timeline. 
    # If no timeline currently opened, get the first timeline, if any, in the project
    timeline = project.GetCurrentTimeline()
    if not timeline:
        if project.GetTimelineCount() > 0:
            timeline = project.GetTimelineByIndex(1)
            project.SetCurrentTimeline(timeline)
        else:
            print("ERROR - There are no timelines. Are you running this script out of the recommended order?")
            return

    # Load the subtitles file.
    try:
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("ERROR - Subtitle file can't be read. Either file permission issue or please check the subtitle path you provided in the script's adjustments.")
        return

    # Split the SRT file content into individual subtitle cues
    # cues = [
    #   "1\n00:00:01,000 --> 00:00:04,000\nHello, world!",
    #   "2\n\n00:00:05,000 --> 00:00:08,000\nThis is a test.",
    #   "3\n00:00:09,000 --> 00:00:12,000\n\nAnother subtitle."
    # ]
    cues = re.split(r"\n{2,}", content.strip())
    
    # Prepare the timecodes so can be parsed
    time_line = re.compile(r"(\d+):(\d+):(\d+),(\d+)\s-->\s(\d+):(\d+):(\d+),(\d+)")

    # Default to no transformations if none provided
    if transformations is None:
        transformations = []

    # Get the start frame of the timeline
    timeline_startframe = timeline.GetStartFrame()

    for cue in cues:
        lines = cue.strip().split("\n")
        if len(lines) >= 3:
            times = lines[1].strip()
            text_lines = lines[2:]

            m = time_line.match(times)
            if not m:
                print(f"ERROR - Failed to parse timing for cue: {times}")
                continue

            t_start = list(map(int, m.groups()[0:4]))
            t_end = list(map(int, m.groups()[4:8]))

            start_seconds = t_start[0] * 3600 + t_start[1] * 60 + t_start[2] + t_start[3] / 1000.0
            end_seconds = t_end[0] * 3600 + t_end[1] * 60 + t_end[2] + t_end[3] / 1000.0

            pos_in_frames = int(start_seconds * frame_rate)
            timeline_pos = timeline_startframe + pos_in_frames

            end_pos_in_frames = int(end_seconds * frame_rate)
            duration = end_pos_in_frames - pos_in_frames

            text = "\n".join(text_lines).strip()

            # Apply user-provided transformation functions
            for transform_func in transformations:
                text = transform_func(text)

            subs.append((timeline_pos, duration, text))

    if(len(subs) == 0):
        print("ERROR - No subtitles found in SRT file or no SRT file found. Please check the srt path you adjusted at this script.")
        return

    print("Will use", len(subs), "subtitles in SRT file to generate Text+ clips on the video track.")

    # Try to get the template Text+
    global media_pool_items_list
    try:
        textplus_media_pool_item = media_pool_items_list[0]
    except IndexError:
        print("ERROR - No Text+ clip found in Media Pool with filename 'text', 'title', or 'subtitle' that would be used as a template.")
        return

    print(f'Will use {textplus_media_pool_item.GetClipProperty()["Clip Name"]} Text+ clip from the media pool as a template to create Text+ clips based off your subtitle cues at video track {TARGET_EMPTY_VIDEO_TRACK}')

    timeline_track = video_track_index

    # Add text+ clips to the timeline
    for i, (timeline_pos, duration, text) in enumerate(subs):
        if i < len(subs) - 1:
            next_timeline_pos = subs[i + 1][0]
            adjusted_duration = next_timeline_pos - timeline_pos
            if adjusted_duration < duration:
                duration = adjusted_duration
        new_clip = {
            "mediaPoolItem": textplus_media_pool_item,
            "startFrame": 0,
            "endFrame": duration,
            "trackIndex": timeline_track,
            "recordFrame": timeline_pos
        }
        media_pool.AppendToTimeline([new_clip])

    # Iterate through the Text+ clips on the track and apply the subtitles to the Text+ clips
    clip_list = timeline.GetItemListInTrack('video', timeline_track)
    subtitle_clips = [clip for clip in clip_list if clip.GetStart() >= subs[0][0]]

    for i, clip in enumerate(subtitle_clips):
        if i >= len(subs):
            break  # No more subtitles to assign

        clip.SetClipColor('Orange')
        text = subs[i][2]

        comp = clip.GetFusionCompByIndex(1)
        if comp:
            tool_found = False
            for tool in comp.GetToolList().values():
                if tool.GetAttrs()['TOOLS_RegID'] == 'TextPlus':
                    tool.SetInput('StyledText', text)
                    tool_found = True
                    break
            if tool_found:
                clip.SetClipColor('Blue')
            else:
                print(f"ERROR - No Text+ tool found in composition for clip at {clip.GetStart()}")
        else:
            print(f"ERROR - No Fusion composition found for clip at {clip.GetStart()}")

    print(f"Text+ clips based on subtitle cues from SRT files have been added to video track #{video_track_index}.")
    print("\nDone!")

generate_text_plus_subtitle_clips(srt_file_path, TARGET_EMPTY_VIDEO_TRACK, frame_rate, transformations=TRANSFORM_EACH_TEXTP)