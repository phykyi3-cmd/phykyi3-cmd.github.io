// Neon Tube Electric Flicker Glow
// Apply to Opacity or Glow Intensity
var flicker = [0, 80, 20, 100, 40, 100, 10, 100];
var idx = Math.floor(time * 24) % flicker.length;
flicker[idx];