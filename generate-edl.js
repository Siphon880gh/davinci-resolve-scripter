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

// Array of slide indexes where you want crossfade between it and the next
const crossfadePositions = [1, 2, 3]; // No crossfade for the last clip

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

        // Ignore crossfade if it's the last clip
        if (crossfadePositions.includes(index) && index !== clipNames.length - 1) {
            let crossfadeDuration = 1; // Define the crossfade duration (in seconds)
            let crossfadeStart = endTime - crossfadeDuration; // Start crossfade before this clip ends

            // Apply crossfade into the next clip
            edl += `${String(index + 1).padStart(3, "0")}  AX       V     C        ${inTime} ${outTime} ${recordInTime} ${secondsToTimecode(crossfadeStart)}\n`;
            edl += `M2   AX             000.0                ${inTime}\n`;
            edl += `* FROM CLIP NAME: ${clipName}\n\n`;

            edl += `${String(index + 1).padStart(3, "0")}  AX       V     D    024 ${inTime} ${outTime} ${secondsToTimecode(crossfadeStart)} ${recordOutTime}\n`;
            edl += `M2   AX             000.0                ${inTime}\n`;
            edl += `M2   AX             000.0                ${inTime}\n`;
            edl += `* TO CLIP NAME: ${clipNames[index + 1]}\n\n`;

            currentTimelineStart += crossfadeDuration; // Adjust the start for the next clip after crossfade
        } else {
            // Regular clip without crossfade
            edl += `${String(index + 1).padStart(3, "0")}  AX       V     C        ${inTime} ${outTime} ${recordInTime} ${recordOutTime}  \n`;
            edl += `M2   AX             000.0                ${inTime}\n`;
            edl += `* FROM CLIP NAME: ${clipName}\n\n`;
        }

        // Update timeline start to match the end of the current clip
        currentTimelineStart = endTime; 
    });

    return edl.trim();
}

// Write file
const generatedEDL = generateEDL(IMAGE_FILES, DESIRED_CLIP_SECONDS, startTimeCode, crossfadePositions);
fs.writeFileSync(outputPath, generatedEDL);
