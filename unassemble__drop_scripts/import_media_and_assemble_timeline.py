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

import os
from constants import ENUM_MEDIA_TYPES, ENUM_IMPORT_MODE

# Common Objects
# ------------------------------------------------
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_pool = project.GetMediaPool()

# Remove timeline block if not applicable
try: 
    timeline = project.GetCurrentTimeline()
except Exception as e: # Comment/Uncomment as needed
    # print("No timeline is currently open.")
    # print(e)
    # exit()
    media_pool.CreateEmptyTimeline("Timeline 1")
    timeline = project.GetCurrentTimeline()
    pass

# _SCRIPT:
# ------------------------------------------------

# Choose the desired start time (format is HH:MM:SS:FF)
START_TIMECODE = "00:00:00:00"  # Set to "00:00:00:00" if needed
# Not doable in free DaVinci

# Setting clip duration fails on free. Just set options in Preferences as a workflow.
DESIRED_CLIP_SECONDS = 40 # Desired duration of each clip in seconds

# Image files (adjust paths if needed)
IMAGE_FILES = [
    "/Users/wengffung/dev/web/davinci/images/clip01.jpg",
    "/Users/wengffung/dev/web/davinci/images/clip02.jpg",
    "/Users/wengffung/dev/web/davinci/images/clip03.jpg",
    "/Users/wengffung/dev/web/davinci/images/clip04.jpg",
    "/Users/wengffung/dev/web/davinci/images/clip05.jpg",
    "/Users/wengffung/dev/web/davinci/images/clip06.jpg",
    "/Users/wengffung/dev/web/davinci/images/clip07.jpg"
]
IMAGE_FOLDERS = ["/Users/wengffung/dev/web/davinci/images/"]

DESIRED_MODE = ENUM_IMPORT_MODE["IMAGE_FILES"] # IMAGE_FILES or IMAGES_FOLDERS

project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()

if project is None:
    print("No project is currently open.")
    exit()

# Get the frame rate from the project settings
frame_rate = project.GetSetting("timelineFrameRate")
if frame_rate is None:
    frame_rate = 24  # Default to 24 fps if not set

# Duration in frames for X seconds (Multiplies frame rate by X seconds)
duration_in_frames = int(DESIRED_CLIP_SECONDS * float(frame_rate))

media_pool = project.GetMediaPool()

# Open the Edit Page
resolve.OpenPage("Edit")

# Set timeline to current one or create a new one if needed
timeline = project.GetCurrentTimeline()
if timeline is None:
    timeline = media_pool.CreateEmptyTimeline("Image Sequence Timeline")
    project.SetCurrentTimeline(timeline)
timeline.SetSetting('timelineFrameRate', str(frame_rate))
timeline.SetSetting("timelineStartFrame", START_TIMECODE) # Not doable in free DaVinci
timeline.SetCurrentTimecode(START_TIMECODE) # Not doable in free DaVinci

# Import the images to the media pool
media_storage = resolve.GetMediaStorage()

imported_clips = []

if( DESIRED_MODE == ENUM_IMPORT_MODE["IMAGE_FILES"] ):
    # Import each image individually
    for image_file in IMAGE_FILES:
        clip = media_pool.ImportMedia([image_file])
        if clip:
            imported_clips.extend(clip)
        else:
            print(f"Failed to import {image_file}")
    print("Imported all images.")

elif( DESIRED_MODE == ENUM_IMPORT_MODE["IMAGE_FOLDERS"] ):   
    # Import all images in the folders
    for image_folder in IMAGE_FOLDERS:
        for root, dirs, files in os.walk(image_folder):
            # Sort directories and files alphabetically
            dirs.sort()
            files.sort()
            for file in files:
                # Get full file path
                image_file = os.path.join(root, file)
                # print(file_path)
                clip = media_pool.ImportMedia([image_file])
                if clip:
                    imported_clips.extend(clip)
                else:
                    print(f"Failed to import {image_file}")

elif( DESIRED_MODE == ENUM_IMPORT_MODE["IMAGE_FOLDERS_ASSEMBLE"] ):   
    # Import all images in the folder
    for image_folder in IMAGE_FOLDERS:
        clip = media_pool.ImportMedia([image_folder])
        if not clip:
            print(f"Failed to import {image_folder}")
    print("Imported all images in folders.")
    clips = timeline.GetItemListInTrack("video", 1)
    for clip in clips:
        # print(clip.GetName())
        imported_clips.extend(clip)

# Prepare the list of clip dictionaries with desired duration
clip_info_list = []

for clip in imported_clips:
    print(clip)
    # For images, the start frame is usually 0, and the end frame determines the duration
    start_frame = 0
    duration_frames = 10  # Desired duration in frames
    end_frame = start_frame + duration_frames - 1  # Subtract 1 because frames are zero-indexed

    # Start frame and end frame may have been removed from DaVinci free. Doesn't throw error
    clip_info = {
        "mediaPoolItem": clip,
        "startFrame": start_frame,
        "endFrame": end_frame,
        "mediaType": ENUM_MEDIA_TYPES["VIDEO"]  # 1 for Video
    }
    clip_info_list.append(clip_info)

# Add the clips to the timeline with the specified duration
success = media_pool.AppendToTimeline(clip_info_list)

if success:
    print("Clips added to the timeline with specified durations.")
else:
    print("Failed to add clips to the timeline.")