// Elastic Gravity Drop Bounce
// Apply to Position
var e = 0.7;
var g = 5000;
var n = 0;
if (numKeys > 0) {
    n = nearestKey(time).index;
    if (key(n).time > time) n--;
}
if (n > 0) {
    var t = time - key(n).time;
    var h = 0.5 * g * t * t;
    value + [0, Math.sin(t * 15) * 50 * Math.exp(-t * 5)];
} else {
    value;
}