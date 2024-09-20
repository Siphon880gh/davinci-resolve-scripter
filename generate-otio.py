import opentimelineio as otio
import os

# Configuration for clips, duration, transitions, and frame rate
IMAGE_FILES = [
    "clip01.jpg", 
    "clip02.jpg", 
    "clip03.jpg", 
    "clip04.jpg", 
    "clip05.jpg"
]
DESIRED_CLIP_SECONDS = 10  # Desired duration of each clip in seconds
FRAME_RATE = 24

# Start timecode (user-defined)
start_time_code = "01:00:00:00"

# Transitions: slide indexes and transition types (D = Dissolve, C = Cut, Wipe = Wipe90)
# Optional: Provide custom transition duration in frames
transition_positions = [
    { "index": 1, "type": "D", "duration": 24 },  # Dissolve with custom duration
    { "index": 2, "type": "D" },                  # Dissolve with default duration
    { "index": 3, "type": "wipe90", "duration": 24 }  # Edge Wipe with angle 90
]

# Default transition settings
DEFAULT_DISSOLVE_DURATION = 24  # Default dissolve duration (frames)

# Create a timeline
timeline = otio.schema.Timeline(name="Example Timeline")
video_track = otio.schema.Track(name="Video Track", kind=otio.schema.TrackKind.Video)
timeline.tracks.append(video_track)

# Create a clip with a specified duration
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
    elif transition_type == "wipe90":
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
clips = []
for i, clip_name in enumerate(IMAGE_FILES):
    clip = create_clip(clip_name, DESIRED_CLIP_SECONDS)
    clips.append(clip)

# Append first clip to the timeline (no transition before the first clip)
video_track.append(clips[0])

# Iterate through clips and apply transitions where specified
for i in range(1, len(clips)):
    # Find the transition type for this clip
    transition_data = next((t for t in transition_positions if t["index"] == i), None)

    if transition_data:
        # Create transition based on specified type and duration
        transition_type = transition_data.get("type", "C")
        transition_duration = transition_data.get("duration", DEFAULT_DISSOLVE_DURATION)
        transition = create_transition(transition_type, in_offset=transition_duration)
    else:
        # Default to cut if no transition specified
        transition = None

    # Add transition (if any) and the next clip
    if transition:
        video_track.append(transition)
    video_track.append(clips[i])

# Ensure the directory exists
output_directory = "generated_otio"
os.makedirs(output_directory, exist_ok=True)

# Save the timeline to a .otio file in the specified directory
output_file_path = os.path.join(output_directory, "generated.otio")
otio.adapters.write_to_file(timeline, output_file_path)

print(f"Timeline created and saved as '{output_file_path}'")
