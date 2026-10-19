// Typewriter with Blinking Cursor
// Apply to Source Text property
var speed = 25; // Characters per second
var cursor = "|"; // Cursor character
var blinkRate = 2; // Blinks per second
var str = "YOUR TYPED TEXT HERE";
var progress = Math.min(Math.floor(time * speed), str.length);
var c = (time * blinkRate) % 1 > 0.5 ? cursor : " ";
if (progress >= str.length) c = (time * blinkRate) % 1 > 0.5 ? cursor : "";
str.substr(0, progress) + c;
