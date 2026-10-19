// 3D Door Swing on Y Axis
// Apply to Y Rotation
var dur = 0.8;
var p = easeOut(time - inPoint, 0, dur, -90, 0);
Math.min(0, p);