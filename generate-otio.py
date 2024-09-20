import opentimelineio as otio
import os

# Configuration for clips, transition settings, and frame rate
IMAGE_FILES = [
    "clip01.jpg", 
    "clip02.jpg", 
    "clip03.jpg", 
    "clip04.jpg", 
    "clip05.jpg"
]
DEFAULT_CLIP_DURATION = 10  # Default duration of each clip in seconds
FRAME_RATE = 24

# Start timecode (user-defined)
start_time_code = "01:00:00:00"

# Clip settings: slide indexes, transition types (D = Dissolve, C = Cut, Wipe90 = Wipe at 90 degrees)
# Optional: Provide custom transition duration using tDuration and clip duration using cDuration
clips_settings = [
    { "index": 0, "type": None, "cDuration": 10 },   # First clip with default duration, no transition
    { "index": 1, "type": "D", "tDuration": 24, "cDuration": 12 },  # Dissolve with custom duration for clip 2
    { "index": 2, "type": "D", "cDuration": 8 },                   # Dissolve with default transition duration for clip 3
    { "index": 3, "type": "Wipe90", "tDuration": 24, "cDuration": 15 },  # Wipe with custom duration for clip 4
    { "index": 4, "type": "C", "cDuration": 10 }                    # Regular cut with default clip duration
]

# Default transition settings
DEFAULT_DISSOLVE_DURATION = 24  # Default dissolve duration (frames)

# Create a timeline
timeline = otio.schema.Timeline(name="Improved Timeline")
video_track = otio.schema.Track(name="Video Track", kind=otio.schema.TrackKind.Video)
timeline.tracks.append(video_track)

# Create a clip with a specified or default duration
def create_clip(name, duration):
    return otio.schema.Clip(
        name=name,
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, FRAME_RATE),
            duration=otio.opentime.RationalTime(duration * FRAME_RATE, FRAME_RATE)
        )
    )

# Create transitions based on type and duration
def create_transition(transition_type, in_offset=None, out_offset=None):
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
    elif transition_type == "Wipe90":
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
                        "Parameter Value": 90,  # Custom angle set to 90 degrees
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

# Ensure the directory exists
output_directory = "generated_otio"
os.makedirs(output_directory, exist_ok=True)

# Save the timeline to a .otio file in the specified directory
output_file_path = os.path.join(output_directory, "generated.otio")
otio.adapters.write_to_file(timeline, output_file_path)

print(f"Timeline created and saved as '{output_file_path}'")
