const IMAGE_FILES = [
    "clip01.jpg", 
    "clip02.jpg", 
    "clip03.jpg", 
    "clip04.jpg", 
    "clip05.jpg"
];
DESIRED_CLIP_SECONDS = 10; // Desired duration of each clip in seconds

const startTimeCode = "01:00:00:00"; // User-defined start timecode for the timeline
let frame_rate = 23;
let outputPath = "./generated_edl/generated.edl"

// Additional parameter: Array of clip positions to apply crossfade
const crossfadePositions = [1]; // For example, add crossfade between clip 1 and clip 2

const fs = require("fs")
function generateEDL(clipNames, durationPerClip, startTimeCode = "00:00:00:00", crossfadePositions = []) {
    let edl = "TITLE: Image Sequence Timeline\nFCM: NON-DROP FRAME\n\n";

    // Helper function to convert timecode in HH:MM:SS:FF format to seconds
    function timecodeToSeconds(timecode) {
        const [hours, mins, secs, frames] = timecode.split(":").map(Number);
        const fps = typeof frame_rate !== "undefined" ? frame_rate : 23; 
        return hours * 3600 + mins * 60 + secs + frames / fps;
    }

    let currentTimelineStart = timecodeToSeconds(startTimeCode); 
    let duration = durationPerClip; 
    
    // Helper function to convert seconds to timecode in HH:MM:SS:FF format
    function secondsToTimecode(seconds) {
        const fps = frame_rate;
        let totalFrames = Math.floor(seconds * fps);
        let frames = totalFrames % fps;
        totalFrames = Math.floor(totalFrames / fps);

        let secs = totalFrames % 60;
        let mins = Math.floor(totalFrames / 60) % 60;
        let hours = Math.floor(totalFrames / 3600);

        return (
            String(hours).padStart(2, "0") + ":" +
            String(mins).padStart(2, "0") + ":" +
            String(secs).padStart(2, "0") + ":" +
            String(frames).padStart(2, "0")
        );
    }

    clipNames.forEach((clipName, index) => {
        let startTime = currentTimelineStart;
        let endTime = currentTimelineStart + duration;

        let inTime = secondsToTimecode(0); 
        let outTime = secondsToTimecode(duration); 
        let recordInTime = secondsToTimecode(startTime); 
        let recordOutTime = secondsToTimecode(endTime); 

        // Check if this clip should have a crossfade transition
        if (crossfadePositions.includes(index)) {
            let crossfadeDuration = 1; // Define the crossfade duration (in seconds)
            let crossfadeEndTime = startTime + crossfadeDuration; 

            // First line for cut (C) without crossfade
            edl += `${String(index + 1).padStart(3, "0")}  AX       V     C        ${inTime} ${outTime} ${recordInTime} ${secondsToTimecode(currentTimelineStart)}  \n`;
            edl += `M2   AX             000.0                ${inTime}\n`;
            edl += `* FROM CLIP NAME: ${clipName}\n\n`;

            // Crossfade (D) from the current clip to the next
            edl += `${String(index + 1).padStart(3, "0")}  AX       V     D    024 ${inTime} ${secondsToTimecode(crossfadeDuration)} ${secondsToTimecode(currentTimelineStart)} ${secondsToTimecode(crossfadeEndTime)}\n`;
            edl += `M2   AX             000.0                ${inTime}\n`;
            edl += `M2   AX             000.0                ${inTime}\n`;
            edl += `* TO CLIP NAME: ${clipNames[index + 1]}\n\n`;

            currentTimelineStart += crossfadeDuration; // Move start time to account for crossfade
        } else {
            edl += `${String(index + 1).padStart(3, "0")}  AX       V     C        ${inTime} ${outTime} ${recordInTime} ${recordOutTime}  \n`;
            edl += `M2   AX             000.0                ${inTime}\n`;
            edl += `* FROM CLIP NAME: ${clipName}\n\n`;
        }

        currentTimelineStart += duration; 
    });

    return edl.trim();
}

// Write file
const generatedEDL = generateEDL(IMAGE_FILES, DESIRED_CLIP_SECONDS, startTimeCode, crossfadePositions);
fs.writeFileSync(outputPath, generatedEDL);
