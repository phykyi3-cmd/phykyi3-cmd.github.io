// Inertial Easing Bounce
// Apply to any property with keyframes (Position, Scale, Rotation)
var n = 0;
if (numKeys > 0){
    n = nearestKey(time).index;
    if (key(n).time > time){ n--; }
}
if (n == 0){
    t = 0;
} else {
    t = time - key(n).time;
}
if (n > 0 && t < 1){
    var v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
    var amp = 0.05;
    var freq = 4.0;
    var decay = 8.0;
    value + v * amp * Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t);
} else {
    value;
}
