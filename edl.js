function generateEDL(clipNames, durationPerClip) {
    let edl = "TITLE: Example EDL for Images\nFCM: NON-DROP FRAME\n\n";
    
    let currentTimelineStart = 0; // Start at 0 seconds
    let duration = durationPerClip; // Fixed duration for each clip in seconds
    
    // Helper function to convert seconds to timecode in HH:MM:SS:FF format
    function secondsToTimecode(seconds) {
        const fps = 30; // Assuming 30 frames per second
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

        let inTime = secondsToTimecode(0); // Fixed 00:00:00:00
        let outTime = secondsToTimecode(duration); // Fixed 00:00:05:00 (duration of 5 seconds)
        let recordInTime = secondsToTimecode(startTime); // Current timeline start
        let recordOutTime = secondsToTimecode(endTime); // Current timeline end

        edl += `${String(index + 1).padStart(3, "0")}  AX       V     C        ${inTime} ${outTime} ${recordInTime} ${recordOutTime}  \n`;
        edl += `M2   AX             000.0                ${inTime}\n`;
        edl += `* FROM CLIP NAME: ${clipName}\n\n`;

        currentTimelineStart += duration; // Move the start time for the next clip
    });

    return edl.trim();
}

// Example usage:
const clipNames = ["clip01.jpg", "clip02.jpg", "clip03.jpg", "clip04.jpg", "clip05.jpg"];
const durationPerClip = 5; // Each clip is 5 seconds
console.log(generateEDL(clipNames, durationPerClip));
