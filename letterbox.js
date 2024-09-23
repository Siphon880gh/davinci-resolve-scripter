const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

// Helper function to create letterboxed image
async function letterboxImage(imagePath, targetWidth, targetHeight, useBlurredBackground) {
    const image = sharp(imagePath);
    const metadata = await image.metadata();

    const imageWidth = metadata.width;
    const imageHeight = metadata.height;
    const aspectRatio = imageWidth / imageHeight;

    let newWidth = Math.floor(targetHeight * aspectRatio);
    let newHeight = targetHeight;

    if (newWidth > targetWidth) {
        newWidth = targetWidth;
        newHeight = Math.floor(targetWidth / aspectRatio);
    }

    const xPadding = Math.floor((targetWidth - newWidth) / 2);
    const yPadding = Math.floor((targetHeight - newHeight) / 2);

    console.log(`Resized image dimensions: ${newWidth}x${newHeight}`);
    console.log(`Padding: x=${xPadding}, y=${yPadding}`);

    let finalImage;

    if (useBlurredBackground) {
        // Create a blurred background from the original image
        const blurScale = 0.1;  // Zoom in more (smaller scale)
        const blurRadius = 30;  // Stronger blur

        // Create a zoomed-in and blurred background image
        const blurredBackground = await image
            .clone()  // Ensure we're not modifying the original image
            .resize(Math.floor(imageWidth * blurScale), Math.floor(imageHeight * blurScale))  // Zoom in
            .blur(blurRadius)  // Apply blur
            .resize(targetWidth, targetHeight)  // Resize to target dimensions (letterbox)
            .toBuffer();

        // Resize the original image for foreground, keeping it sharp
        const resizedForeground = await image
            .clone()  // Clone to avoid blurring the foreground
            .resize(newWidth, newHeight)  // Resize the foreground image to fit the target
            .toBuffer();

        // Composite the sharp foreground onto the blurred background
        finalImage = await sharp(blurredBackground)
            .composite([{ input: resizedForeground, top: yPadding, left: xPadding }])  // Overlay the sharp image
            .toBuffer();
    } else {
        // Use black bars for letterboxing if no background is blurred
        const resizedImage = await image.resize(newWidth, newHeight).toBuffer();
        finalImage = await sharp({
            create: {
                width: targetWidth,
                height: targetHeight,
                channels: 4,
                background: { r: 0, g: 0, b: 0, alpha: 1 },
            },
        })
        .composite([{ input: resizedImage, top: yPadding, left: xPadding }])
        .toBuffer();
    }

    // Save the image
    const savePath = path.join(path.dirname(imagePath), `${path.basename(imagePath, path.extname(imagePath))}_letterboxed.png`);
    await sharp(finalImage).toFile(savePath);
    console.log(`Saved letterboxed image to: ${savePath}`);
}

// Function to process a list of images
async function letterboxAndSaveImages(imagePaths, useBlurredBackground = false) {
    const images = await Promise.all(imagePaths.map(p => sharp(p).metadata()));

    // Determine the largest image by area
    const maxDimensions = images.reduce((max, img) => {
        return img.width * img.height > max.width * max.height ? img : max;
    }, images[0]);

    const targetWidth = maxDimensions.width;
    const targetHeight = maxDimensions.height;

    console.log(`Calculated letterbox max dimensions: ${targetWidth}x${targetHeight}`);

    for (let imagePath of imagePaths) {
        await letterboxImage(imagePath, targetWidth, targetHeight, useBlurredBackground);
    }
}

// Example usage
const imagePaths = [
    './letterbox_test/clip01.jpg',
    './letterbox_test/clip02.jpg',
    './letterbox_test/clip03.jpg',
    './letterbox_test/clip04.jpg',
    './letterbox_test/clip05.jpg',
    './letterbox_test/clip06.jpg',
    './letterbox_test/clip07.jpg'
];

letterboxAndSaveImages(imagePaths, true)
    .then(() => console.log('All images processed successfully'))
    .catch(err => console.error('Error processing images:', err));
