const fs = require('fs');

const IMAGE_FILES = [
    "clip01.jpg", 
    "clip02.jpg", 
    "clip03.jpg", 
    "clip04.jpg", 
    "clip05.jpg"
];
const DESIRED_CLIP_SECONDS = 10; // Desired duration of each clip in seconds
const startTimeCode = "01:00:00:00"; // User-defined start timecode for the timeline
const frame_rate = 24; // Ensure frame rate matches DaVinci Resolve settings
const outputPath = "./generated_otio/generated.otio";

// Array of slide indexes where you want specific transitions applied
const transitionPositions = [
    {index: 1, type: "D", duration: 24},  // Dissolve with duration
    {index: 2, type: "WR"},               // Wipe Right (Edge Wipe with angle 90)
    {index: 3, type: "WU"},               // Wipe Up (Edge Wipe with angle 0)
    {index: 4, type: "WL"}                // Wipe Left (Edge Wipe with angle -90)
];

const DEFAULT_DISSOLVE_DURATION = 24; // Default duration for dissolve if not provided

// Wipe direction angles based on type
const wipeAngles = {
    'WU': 0,    // Wipe Up
    'WR': 90,   // Wipe Right
    'WL': -90,  // Wipe Left
    'WD': 180   // Wipe Down
};

// Function to convert startTimeCode into a RationalTime for global_start_time
function timecodeToRationalTime(timecode, fps) {
    const [hours, minutes, seconds, frames] = timecode.split(":").map(Number);
    const totalSeconds = hours * 3600 + minutes * 60 + seconds + frames / fps;
    return { 
        "OTIO_SCHEMA": "RationalTime.1",
        "value": Math.floor(totalSeconds * fps),
        "rate": fps 
    };
}

// Function to create TimeRange objects
function createTimeRange(start, duration, fps) {
    return {
        "OTIO_SCHEMA": "TimeRange.1",
        "start_time": {
            "OTIO_SCHEMA": "RationalTime.1",
            "value": start,
            "rate": fps
        },
        "duration": {
            "OTIO_SCHEMA": "RationalTime.1",
            "value": duration,
            "rate": fps
        }
    };
}

// Function to create Clip objects for OTIO
function createClip(name, duration, fps) {
    return {
        "OTIO_SCHEMA": "Clip.1",
        "name": name,
        "available_range": createTimeRange(0, duration, fps),
        "type": "Clip"
    };
}

// Function to create Dissolve transitions
function createDissolveTransition(name, in_offset, out_offset) {
    return {
        "OTIO_SCHEMA": "Transition.1",
        "name": name,
        "transition_type": "Dissolve",
        "in_offset": {
            "OTIO_SCHEMA": "RationalTime.1",
            "value": in_offset,
            "rate": frame_rate
        },
        "out_offset": {
            "OTIO_SCHEMA": "RationalTime.1",
            "value": out_offset,
            "rate": frame_rate
        },
        "type": "Transition"
    };
}

// Function to create Edge Wipe transitions
function createEdgeWipeTransition(name, type, in_offset, out_offset) {
    const angle = wipeAngles[type];
    return {
        "OTIO_SCHEMA": "Transition.1",
        "name": name,
        "transition_type": "Custom_Transition",
        "in_offset": {
            "OTIO_SCHEMA": "RationalTime.1",
            "value": in_offset,
            "rate": frame_rate
        },
        "out_offset": {
            "OTIO_SCHEMA": "RationalTime.1",
            "value": out_offset,
            "rate": frame_rate
        },
        "metadata": {
            "Resolve_OTIO": {
                "Effects": {
                    "Effect Name": "Edge Wipe",
                    "Enabled": true,
                    "Name": "Edge Wipe",
                    "Parameters": [
                        {
                            "Default Parameter Value": 0,
                            "Key Frames": {},
                            "Parameter ID": "angle",
                            "Parameter Value": angle,
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
                                "24": { // Assuming transition duration is 24 frames
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
                    "Type": 13
                },
                "Transition Type": "Edge Wipe"
            }
        },
        "type": "Transition"
    };
}

// Start building the OTIO timeline object
let timeline = {
    "OTIO_SCHEMA": "Timeline.1",
    "metadata": {
        "Resolve_OTIO": {
            "Resolve OTIO Meta Version": "1.0"
        }
    },
    "name": "Generated Timeline",
    "global_start_time": timecodeToRationalTime(startTimeCode, frame_rate),
    "tracks": [
        {
            "OTIO_SCHEMA": "Track.1",
            "name": "Video Track",
            "kind": "Video",
            "children": [],
            "type": "Track"
        }
    ],
    "type": "Timeline.1"
};

// Add clips and transitions to the track
IMAGE_FILES.forEach((fileName, index) => {
    // Create a clip and add it to the timeline
    const clip = createClip(fileName, DESIRED_CLIP_SECONDS, frame_rate);
    timeline.tracks[0].children.push(clip);

    // Check if there's a transition for the current clip
    const transition = transitionPositions.find(t => t.index === index);
    if (transition) {
        const transitionDuration = transition.duration || DEFAULT_DISSOLVE_DURATION;
        const in_offset = Math.floor(transitionDuration / 2);
        const out_offset = Math.floor(transitionDuration / 2);

        let transitionObj = null;
        if (transition.type === "D") {
            transitionObj = createDissolveTransition("Dissolve", in_offset, out_offset);
        } else if (['WU', 'WR', 'WL', 'WD'].includes(transition.type)) {
            transitionObj = createEdgeWipeTransition("Edge Wipe", transition.type, in_offset, out_offset);
        }

        if (transitionObj) {
            timeline.tracks[0].children.push(transitionObj);
        }
    }
});

// Save the OTIO JSON to a file
fs.writeFileSync(outputPath, JSON.stringify(timeline, null, 4));

console.log(`OTIO file generated at ${outputPath}`);
