var socket = io.connect('http://' + document.domain + ':' + location.port);

function encode(input) {
    var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var output = "";
    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
    var i = 0;

    while (i < input.length) {
        chr1 = input[i++];
        chr2 = i < input.length ? input[i++] : Number.NaN; // Not sure if the index
        chr3 = i < input.length ? input[i++] : Number.NaN; // checks are needed here

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
            enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
            enc4 = 64;
        }
        output += keyStr.charAt(enc1) + keyStr.charAt(enc2) +
            keyStr.charAt(enc3) + keyStr.charAt(enc4);
    }
    return output;
}

// Everything else after page load.
$(function () {
    if (window.JpegCamera) {
        var camera;

        var options = {
            shutter_ogg_url: "static/library/jpeg_camera/shutter.ogg",
            shutter_mp3_url: "static/library/jpeg_camera/shutter.mp3",
            swf_url: "static/library/jpeg_camera/jpeg_camera.swf"
        };

        var upload_stream = function () {
            var snapshot = camera.capture();
            snapshot.get_blob(function (blob) {
                socket.emit('image_feed_', {data: blob});
            }, "image/jpeg");
        };

        camera = new JpegCamera("#camera", options).ready(function (info) {

        });

        setInterval(upload_stream, 1500);
    }

    socket.on('video_stream', function (message) {
        var bytes = new Uint8Array(message.data);
        $("#bg").attr("src", 'data:image/png;base64,' + encode(bytes));
    });
});


