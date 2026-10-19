function main() {
    app.beginUndoGroup("Sticker Screen Fill Animated");

    var comp = app.project.activeItem;
    if (!(comp instanceof CompItem)) {
        alert("Select a composition.");
        return;
    }

    var sticker = comp.layer("STICKER");
    if (!sticker) {
        alert("Layer named 'STICKER' not found.");
        return;
    }

    //user controls
    var STICKER_COUNT = 90;     // increase for denser coverage
    var ANIM_DURATION = 0.09;    // scale animation length (seconds)
    var STAGGER = 0.02;          // delay between stickers
    var SCALE_MIN = 60;
    var SCALE_MAX = 120;

    var compW = comp.width;
    var compH = comp.height;
    var startTime = comp.time;

    var scaleProp = sticker.property("Scale");
    var is3D = scaleProp.value.length === 3;

    for (var i = 0; i < STICKER_COUNT; i++) {
        var dup = sticker.duplicate();

        // random pos across entire composition
        dup.property("Position").setValue([
            Math.random() * compW,
            Math.random() * compH
        ]);

        // random rotation
        dup.property("Rotation").setValue(Math.random() * 360);

        // random scale
        var finalScale = SCALE_MIN + Math.random() * (SCALE_MAX - SCALE_MIN);
        var scaleValue = is3D
            ? [finalScale, finalScale, finalScale]
            : [finalScale, finalScale];

        var s = dup.property("Scale");

        var t0 = startTime + i * STAGGER;
        var t1 = t0 + ANIM_DURATION;

        
        s.setValueAtTime(t0, is3D ? [0, 0, 0] : [0, 0]);
        s.setValueAtTime(t1, scaleValue);

        // proper ease array length
        var ease = new KeyframeEase(0, 80);
        var easeArray = is3D ? [ease, ease, ease] : [ease, ease];

        s.setTemporalEaseAtKey(2, easeArray, easeArray);
    }

    sticker.enabled = false;
    app.endUndoGroup();
}

main();
