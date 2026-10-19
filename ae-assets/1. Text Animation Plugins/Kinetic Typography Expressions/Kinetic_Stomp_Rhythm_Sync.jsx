// Stomp Rhythm Typography Expression
// Syncs scale snaps to beat markers
var m = thisComp.marker;
var t = time;
var scaleSnap = 100;
if (m.numKeys > 0) {
    var k = m.nearestKey(t);
    var diff = Math.abs(t - k.time);
    if (diff < 0.1) {
        scaleSnap = easeOut(diff, 0, 0.1, 140, 100);
    }
}
[scaleSnap, scaleSnap];