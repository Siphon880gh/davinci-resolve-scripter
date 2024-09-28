# pip install opentimelineio==0.17.0

import opentimelineio as otio
import os
import json

# _ADJUST the abs path to the app.clips.json, due to limitation of free DaVinci - 1 of 7
APP_CLIPS_JSON_ABS_PATH = "/Users/wengffung/dev/web/davinci/app.clips.json"

# _ADJUST ../app.clips.json instead - 2 of 7
# Clip file names
# IMAGE_FILES = [
#     "clip01.jpg", 
#     "clip02.jpg"
#     ..
# ]
def get_image_paths():
    global APP_CLIPS_JSON_ABS_PATH
    with open(APP_CLIPS_JSON_ABS_PATH, 'r') as f:
        clips_config = json.load(f)

    image_abs_path = clips_config['image_abs_path']
    
    # Ensure the path ends with a forward slash
    if not image_abs_path.endswith('/'):
        image_abs_path += '/'

    clip_basenames = clips_config['clip_basenames']
    clip_basenames = [os.path.join(image_abs_path, clip_basename) for clip_basename in clip_basenames]

    return clip_basenames
IMAGE_FILES = get_image_paths()

# _ADJUST ../app.clips.json instead - 3 of 7
# Path to the folder where the clip files are stored
def get_image_folder():
    global APP_CLIPS_JSON_ABS_PATH
    with open(APP_CLIPS_JSON_ABS_PATH, 'r') as f:
        clips_config = json.load(f)

    image_abs_path = clips_config['image_abs_path']
    
    # Ensure the path ends with a forward slash
    if not image_abs_path.endswith('/'):
        image_abs_path += '/'

    return image_abs_path
MEDIA_FOLDER = get_image_folder()

# _ADJUST the transitions you want at after which clip - 4 of 7
# Clip settings: slide indexes, transition types (D = Dissolve, C = Cut, WipeUp = Wipe at 0 degrees, etc.)
# Optional: Provide custom transition duration using tDuration and clip duration using cDuration
clips_settings = [
    { "index": 0, "type": None, "cDuration": 10 },   # First clip with default duration, no transition
    { "index": 1, "type": "D", "tDuration": 24, "cDuration": 12 },  # Dissolve with custom duration for clip 2
    { "index": 2, "type": "WipeRight", "tDuration": 24, "cDuration": 8 },  # WipeRight (90 degrees)
    { "index": 3, "type": "WipeLeft", "tDuration": 24, "cDuration": 15 },  # WipeLeft (-90 degrees)
    { "index": 4, "type": "WipeUp", "tDuration": 24, "cDuration": 10 }    # WipeUp (0 degrees)
]


# _ADJUST each clip duration and frame rate - 5 of 7
DEFAULT_CLIP_DURATION = 10  # Default duration of each clip in seconds
FRAME_RATE = 24

# _ADJUST starting timecode - 6 of 7
# Recommend start at 0 if you will run motion effects script
start_time_code = "00:00:00:00"

# _ADJUST default transition settings - 7 of 7
# If cDuration not defined in a clip's clip_settings, this setting applies.
DEFAULT_DISSOLVE_DURATION = 24  # Default dissolve duration (frames)

# Create a timeline
timeline = otio.schema.Timeline(name="Enhanced Timeline")
video_track = otio.schema.Track(name="Video Track", kind=otio.schema.TrackKind.Video)
timeline.tracks.append(video_track)

# Create a clip with a specified or default duration and a full path
def create_clip(file_name, duration):
    # Construct the full path to the media file
    full_file_path = os.path.join(MEDIA_FOLDER, file_name)

    # Create an ExternalReference for the media file
    media_reference = otio.schema.ExternalReference(
        target_url=f"file://{full_file_path}",
        available_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, FRAME_RATE),
            duration=otio.opentime.RationalTime(duration * FRAME_RATE, FRAME_RATE)
        )
    )

    # Create the clip with the media reference
    return otio.schema.Clip(
        name=file_name,
        media_reference=media_reference,
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, FRAME_RATE),
            duration=otio.opentime.RationalTime(duration * FRAME_RATE, FRAME_RATE)
        )
    )

# Create transitions based on type and duration
def create_transition(transition_type, in_offset=None, out_offset=None):
    angle = None
    
    # Determine the angle for edge wipes
    if transition_type == "WipeRight":
        angle = 90
    elif transition_type == "WipeLeft":
        angle = -90
    elif transition_type == "WipeUp":
        angle = 0
    elif transition_type == "WipeDown":
        angle = 180

    if transition_type == "D":
        # Dissolve transition (default or custom duration)
        in_offset = otio.opentime.RationalTime(in_offset if in_offset else DEFAULT_DISSOLVE_DURATION, FRAME_RATE)
        out_offset = in_offset
        return otio.schema.Transition(
            transition_type=otio.schema.TransitionTypes.SMPTE_Dissolve,
            in_offset=in_offset,
            out_offset=out_offset
        )
    elif transition_type == "C":
        # Cut transition (no need to define an actual transition)
        return None
    elif angle is not None:
        # Create an edge wipe transition with metadata for DaVinci Resolve
        transition = otio.schema.Transition(
            transition_type="Custom_Transition",  # Custom type for wipe
            in_offset=otio.opentime.RationalTime(in_offset if in_offset else DEFAULT_DISSOLVE_DURATION, FRAME_RATE),
            out_offset=otio.opentime.RationalTime(out_offset if out_offset else DEFAULT_DISSOLVE_DURATION, FRAME_RATE)
        )

        # Adding custom metadata for DaVinci Resolve to recognize the Edge Wipe with angle and curves
        transition.metadata["Resolve_OTIO"] = {
            "Effects": {
                "Effect Name": "Edge Wipe",
                "Enabled": True,
                "Name": "Edge Wipe",
                "Parameters": [
                    {
                        "Default Parameter Value": 0,
                        "Key Frames": {},
                        "Parameter ID": "angle",
                        "Parameter Value": angle,  # Custom angle set based on type
                        "Variant Type": "Int",
                        "maxValue": 360.0,
                        "minValue": -360.0
                    },
                    {
                        "Default Parameter Value": 0.0,
                        "Key Frames": {
                            "0": {
                                "Value": 0.0,
                                "Variant Type": "Double"
                            },
                            "24": {
                                "Value": 1.0,
                                "Variant Type": "Double"
                            }
                        },
                        "Parameter ID": "transitionCustomCurvesKeyframes",
                        "Parameter Value": 0.0,
                        "Variant Type": "Double",
                        "maxValue": 1.0,
                        "minValue": 0.0
                    }
                ],
                "Type": 13  # Specific to edge wipe in DaVinci Resolve
            },
            "Transition Type": "Edge Wipe"
        }
        return transition
    else:
        # Fallback to a cut if an unknown transition type is given
        return None

# Initialize clips and transitions
for clip_data in clips_settings:
    clip_index = clip_data["index"]

    # Ensure the clip index exists within IMAGE_FILES
    if clip_index < len(IMAGE_FILES):
        clip_name = IMAGE_FILES[clip_index]
        clip_duration = clip_data.get("cDuration", DEFAULT_CLIP_DURATION)
        
        clip = create_clip(clip_name, clip_duration)
        video_track.append(clip)

        # For all clips after the first, add a transition if specified
        if clip_index > 0:
            transition_type = clip_data.get("type", "C")
            transition_duration = clip_data.get("tDuration", DEFAULT_DISSOLVE_DURATION)
            transition = create_transition(transition_type, in_offset=transition_duration)
            
            if transition:
                video_track.append(transition)
    else:
        print(f"Warning: clip index {clip_index} is out of range for IMAGE_FILES.")

# Ensure the directory exists
output_directory = "generated_otio"
os.makedirs(output_directory, exist_ok=True)

# Save the timeline to a .otio file in the specified directory
output_file_path = os.path.join(output_directory, "generated.otio")
otio.adapters.write_to_file(timeline, output_file_path)

print(f"Timeline created and saved as '{output_file_path}'")
