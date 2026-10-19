// Bounce & Overshoot Expression for Scale & Position
// Apply to Scale or Position property
var freq = 3.0; // Oscillations per second
var decay = 5.0; // Decay speed
var n = 0;
if (numKeys > 0) {
    n = nearestKey(time).index;
    if (key(n).time > time) n--;
}
if (n > 0) {
    var t = time - key(n).time;
    var amp = velocityAtTime(key(n).time - 0.001);
    var w = freq * Math.PI * 2;
    value + (amp * (Math.sin(t * w) / Math.exp(decay * t))) / w;
} else {
    value;
}
