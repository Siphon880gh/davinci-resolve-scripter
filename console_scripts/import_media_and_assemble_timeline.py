import os
import sys
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples')

# Media types
ENUM_MEDIA_TYPES = {
    "VIDEO": 1,
    "AUDIO": 2,
    "AUDIOVISUAL": 3,
    "SUBTITLE": 4,
}

# Import from image files or folders
ENUM_IMPORT_MODE = {
    "IMAGE_FILES": 1,
    "IMAGE_FOLDERS": 2, # image01, image02 => clip[01-02]
    "IMAGE_FOLDERS_ASSEMBLE": 3, # image01, image02 => clip[01-02]
}

from python_get_resolve import GetResolve
resolve = app.GetResolve()

if resolve is None:
    print("Failed to connect to DaVinci Resolve.")
    exit()


# Setting clip duration fails on free. Just set options in Preferences as a workflow.
DESIRED_CLIP_SECONDS = 10 # Desired duration of each clip in seconds

# Image files (adjust paths if needed)
IMAGE_FILES = [
    "/Users/wengffung/Downloads/DaVinci Assets 2/clip01.jpg",
    "/Users/wengffung/Downloads/DaVinci Assets 2/clip02.jpg",
    "/Users/wengffung/Downloads/DaVinci Assets 2/clip03.jpg",
    "/Users/wengffung/Downloads/DaVinci Assets 2/clip04.jpg",
    "/Users/wengffung/Downloads/DaVinci Assets 2/clip05.jpg",
    "/Users/wengffung/Downloads/DaVinci Assets 2/clip06.jpg",
    "/Users/wengffung/Downloads/DaVinci Assets 2/clip07.jpg"
]
IMAGE_FOLDERS = ["/Users/wengffung/Downloads/DaVinci Assets 2/"]

DESIRED_MODE = ENUM_IMPORT_MODE["IMAGE_FOLDERS"] # IMAGE_FILES or IMAGES_FOLDERS

project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()

if project is None:
    print("No project is currently open.")
    exit()

# Get the frame rate from the project settings
frame_rate = project.GetSetting("timelineFrameRate")
if frame_rate is None:
    frame_rate = 23  # Default to 23 fps if not set

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