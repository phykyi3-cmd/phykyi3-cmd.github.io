// Currency Counter (zsh to ,000,000)
// Apply to Source Text
var target = 1000000;
var dur = 2.5;
var cur = Math.min(target, Math.floor(easeOut(time - inPoint, 0, dur, 0, target)));
"$" + cur.toLocaleString();