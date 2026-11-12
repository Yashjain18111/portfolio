// Hero: a slow-moving telemetry trace. Static if the visitor prefers reduced motion.
(function () {
    var line = document.getElementById("trace-line");
    if (line) {
        var N = 120, W = 1200, H = 140;
        var data = [];
        var t = 0;

        function sample() {
            t += 1;
            var v = 70 + Math.sin(t / 7) * 18 + Math.sin(t / 2.3) * 6 + (Math.random() - 0.5) * 8;
            if (Math.random() < 0.035) v -= 40 + Math.random() * 20; // occasional spike
            return Math.max(8, Math.min(H - 8, v));
        }

        function draw() {
            var step = W / (N - 1), pts = "";
            for (var i = 0; i < data.length; i++) {
                pts += (i * step).toFixed(1) + "," + data[i].toFixed(1) + " ";
            }
            line.setAttribute("points", pts.trim());
        }

        for (var i = 0; i < N; i++) data.push(sample());
        draw();

        var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (!reduce) {
            setInterval(function () {
                data.shift();
                data.push(sample());
                draw();
            }, 140);
        }
    }

    // After a failed contact submit the page re-renders at the top; jump to the form.
    if (document.querySelector("[data-has-errors]")) {
        var contact = document.getElementById("contact");
        if (contact) contact.scrollIntoView();
    }
})();
