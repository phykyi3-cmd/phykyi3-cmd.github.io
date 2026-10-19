// Alex Hormozi Style Word Color Highlight
// Apply to Fill Color property animator
var activeWord = Math.floor((time - inPoint) * 3);
if (textIndex == activeWord) {
    [1, 0.85, 0, 1]; // Vibrant Yellow highlight
} else {
    [1, 1, 1, 1];    // White
}