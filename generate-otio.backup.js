const fs = require('fs');

const IMAGE_FILES = [
    "clip01.mp4", 
    "clip02.mp4", 
    "clip03.mp4", 
    "clip04.mp4", 
    "clip05.mp4"
];
const DESIRED_CLIP_SECONDS = 10; // Desired duration of each clip in seconds
const startTimeCode = "01:00:00:00"; // User-defined start timecode for the timeline
let frame_rate = 23;
let outputPath = "./generated_otio/example_timeline.otio";

// Array of slide indexes where you want specific transitions applied
const transitionPositions = [
    {index: 1, type: "D", duration: 24},  // Dissolve with duration
    {index: 2, type: "W"},                // Wipe with default duration
    {index: 3, type: "C"}                 // Regular Cut
];

const DEFAULT_DISSOLVE_DURATION = 24; // Default duration for dissolve if not provided

// Helper function to convert timecode in HH:MM:SS:FF format to RationalTime in OTIO format
function timecodeToRationalTime(timecode, fps) {
    const [hours, minutes, seconds, frames] = timecode.split(":").map(Number);
    const totalSeconds = hours * 3600 + minutes * 60 + seconds + frames / fps;
    return { value: totalSeconds * fps, rate: fps };
}

// Function to create clip objects for OTIO
function createClip(name, duration, fps) {
    return {
        "name": name,
        "available_range": {
            "start_time": { "value": 0, "rate": fps },
            "duration": { "value": duration * fps, "rate": fps }
        },
        "type": "Clip"
    };
}

// Function to create transition objects for OTIO
function createTransition(type, in_offset, out_offset) {
    let transitionType = "";
    if (type === "D") transitionType = "Dissolve";
    if (type === "W") transitionType = "Wipe";

    return {
        "name": transitionType,
        "transition_type": transitionType,
        "in_offset": { "value": in_offset, "rate": frame_rate },
        "out_offset": { "value": out_offset, "rate": frame_rate },
        "type": "Transition"
    };
}

// Start building the OTIO timeline object
let timeline = {
    "name": "Generated Timeline",
    "tracks": [
        {
            "name": "Video Track",
            "kind": "Video",
            "children": []
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
        const in_offset = transition.duration || DEFAULT_DISSOLVE_DURATION;
        const out_offset = transition.duration || DEFAULT_DISSOLVE_DURATION;

        // Add the transition to the track
        const transitionObj = createTransition(transition.type, in_offset, out_offset);
        timeline.tracks[0].children.push(transitionObj);
    }
});

// Save the OTIO-like JSON to a file
fs.writeFileSync(outputPath, JSON.stringify(timeline, null, 4));

console.log(`OTIO file generated at ${outputPath}`);
