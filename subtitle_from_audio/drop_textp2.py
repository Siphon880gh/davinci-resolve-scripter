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

# ADJUST 1 of 4
SRT_FILENAME = "drop_subtitle_media.srt"


# ADJUST 2 of 4
# Note you have to write the absolute path to the SRT file
# Why: `os.path.dirname(os.path.abspath(__name__)) would fail because it's a 
# drop in script into DaVinci Resolve console which will change __name__ abs pathing 
# to /Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/..
SCRIPT_DIR = "/Users/wengffung/dev/web/davinci/subtitle_from_audio/"
if not os.path.exists(SCRIPT_DIR):
    SCRIPT_DIR = "/Users/wengffung/dev/web/davinci/05_subtitle_from_audio/"
srt_file_path = os.path.join(SCRIPT_DIR, SRT_FILENAME)
print(f"Reading SRT file from: {srt_file_path}")


# ADJUST 3 of 4
# Make sure you have an empty video track to insert the Text+ based off subtitles
video_track_index = 2


# ADJUST 4 of 4
# Adjust text transformations, if any, to apply to each Text+ clip's text
# Eg. TRANSFORM_EACH_TEXTP = [uppercase_all]
# Eg. TRANSFORM_EACH_TEXTP = [uppercase_first_word]
# Eg. TRANSFORM_EACH_TEXTP = [uppercase_tagged_text] # Eg. <u>Word<u> becomes WORD
# Eg. TRANSFORM_EACH_TEXTP = [uppercase_first_word, uppercase_tagged_text]
# Eg. TRANSFORM_EACH_TEXTP = []
transformations = [uppercase_tagged_text]

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

def GenerateTextPlusSubtitles(srt_path, video_track_index, frame_rate=None, transformations=None):
    content = ''
    subs = []

    # Initialize Resolve and Project
    # resolve = bmd.scriptapp("Resolve")
    # project_manager = resolve.GetProjectManager()
    # project = project_manager.GetCurrentProject()
    mediaPool = media_pool

    if not project:
        print("No project is loaded")
        return

    resolve.OpenPage("edit")

    # Get current timeline. If no current timeline, try to load it from timeline list
    timeline = project.GetCurrentTimeline()
    if not timeline:
        if project.GetTimelineCount() > 0:
            timeline = project.GetTimelineByIndex(1)
            project.SetCurrentTimeline(timeline)
        else:
            print("Current project has no timelines")
            return

    # Get frame rate
    if frame_rate is None:
        frame_rate = timeline.GetSetting('timelineFrameRate')
        frame_rate = float(frame_rate) if frame_rate else 24.0  # Default to 24 FPS if not set
    else:
        frame_rate = float(frame_rate)

    # Load the subtitles file.
    try:
        with open(srt_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("ERROR - Subtitle file can't be read. Please check the subtitle path.")
        return

    # Split the SRT file content into individual subtitle cues
    cues = re.split(r"\n{2,}", content.strip())

    # Prepare the timecodes for parsing
    time_line = re.compile(r"(\d+):(\d+):(\d+),(\d+)\s-->\s(\d+):(\d+):(\d+),(\d+)")

    # Default to no transformations if none provided
    if transformations is None:
        transformations = []

    # Get the start frame of the timeline
    timeline_startframe = timeline.GetStartFrame()

    expanded_subs = []  # New list to hold all phrases with timings

    for cue in cues:
        lines = cue.strip().split("\n")
        if len(lines) >= 3:
            times = lines[1].strip()
            text_lines = lines[2:]

            m = time_line.match(times)
            if not m:
                print(f"Failed to parse timing for cue: {times}")
                continue

            t_start = list(map(int, m.groups()[0:4]))
            t_end = list(map(int, m.groups()[4:8]))

            start_seconds = t_start[0] * 3600 + t_start[1] * 60 + t_start[2] + t_start[3] / 1000.0
            end_seconds = t_end[0] * 3600 + t_end[1] * 60 + t_end[2] + t_end[3] / 1000.0

            posInFrames = int(start_seconds * frame_rate)
            timeline_pos = timeline_startframe + posInFrames

            endPosInFrames = int(end_seconds * frame_rate)
            duration = endPosInFrames - posInFrames

            # Replace newlines with special token
            text = "\n".join(text_lines).strip()
            text = text.replace('\n', ' __nl__ ')

            # Apply user-provided transformation functions
            for transform_func in transformations:
                text = transform_func(text)

            words = text.split()
            if not words:
                continue  # Skip empty subtitles

            # Accumulate words into cumulative phrases
            cumulative_phrases = []
            current_phrase = ''
            for word in words:
                if word == '__nl__':
                    current_phrase += '\n'
                else:
                    if current_phrase and not current_phrase.endswith('\n'):
                        current_phrase += ' '
                    current_phrase += word
                cumulative_phrases.append(current_phrase.strip())

            # Determine duration for each phrase
            phrase_count = len(cumulative_phrases)
            if phrase_count == 0:
                continue  # Skip if no phrases

            phrase_duration = duration // phrase_count
            remainder = duration % phrase_count

            for i, phrase in enumerate(cumulative_phrases):
                phrase_start = timeline_pos + i * phrase_duration
                # Add remainder frames to the last phrase
                if i == phrase_count - 1:
                    adjusted_duration = phrase_duration + remainder
                else:
                    adjusted_duration = phrase_duration

                # Replace special token with newline
                phrase = phrase.replace('__nl__', '\n')

                expanded_subs.append((phrase_start, adjusted_duration, phrase))

    if len(expanded_subs) == 0:
        print("No subtitles found after processing.")
        return

    print("Generated", len(expanded_subs), "phrases for subtitles")

    # Ensure media_pool_items_list is populated
    global media_pool_items_list
    if not media_pool_items_list:
        print("No Text+ templates found. Ensure 'init_by_finding_textp_clip_in_media_pool' has been called.")
        return

    # Try to get the template Text+
    try:
        textplus_media_pool_item = media_pool_items_list[0]
    except IndexError:
        print("No Text+ template found in Media Pool matching 'text', 'title', or 'subtitle'.")
        return

    print(f'Using {textplus_media_pool_item.GetClipProperty()["Clip Name"]} as template for Text+ clips.')

    timeline_track = video_track_index

    # Add Text+ clips to the timeline
    for i, (timeline_pos, duration, text) in enumerate(expanded_subs):
        new_clip = {
            "mediaPoolItem": textplus_media_pool_item,
            "startFrame": 0,
            "endFrame": duration,
            "trackIndex": timeline_track,
            "recordFrame": timeline_pos
        }
        media_pool.AppendToTimeline([new_clip])

    # Modify subtitle text content in the clips
    clipList = timeline.GetItemListInTrack('video', timeline_track)
    subtitle_clips = [clip for clip in clipList if clip.GetStart() >= expanded_subs[0][0]]

    for i, clip in enumerate(subtitle_clips):
        if i >= len(expanded_subs):
            break  # No more phrases to assign

        clip.SetClipColor('Orange')
        text = expanded_subs[i][2]

        # Ensure any remaining special tokens are replaced
        text = text.replace('__nl__', '\n')

        comp = clip.GetFusionCompByIndex(1)
        if comp:
            tool_found = False
            for tool in comp.GetToolList().values():
                if tool.GetAttrs()['TOOLS_RegID'] == 'TextPlus':
                    tool.SetInput('StyledText', text)
                    tool_found = True
                    break
            if tool_found:
                clip.SetClipColor('Teal')
            else:
                print(f"No Text+ tool found in composition for clip at {clip.GetStart()}")
        else:
            print(f"No Fusion composition found for clip at {clip.GetStart()}")

    print(f"Text+ clips based on subtitle cues from SRT file have been added to video track {video_track_index}.")
    print("\nDone!")

# Main execution
# if __name__ == "__main__":
#     # Initialize Resolve and Project
#     resolve = bmd.scriptapp("Resolve")
#     project_manager = resolve.GetProjectManager()
#     project = project_manager.GetCurrentProject()

#     if not project:
#         print("No project is loaded")
#     else:
#         # Identify Text+ templates in the Media Pool
#         IdentityTemplateInMediaPool()

#         # Path to your SRT file
#         srt_path = "path/to/your/subtitles.srt"

#         # Video track index where you want to add the subtitles (e.g., 2)
#         video_track_index = 2

# Call the function
GenerateTextPlusSubtitles(srt_file_path, video_track_index, transformations=transformations)