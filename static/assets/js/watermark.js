$(document).ready(function () {
    let isDragging = false;
    let offsetX, offsetY;
    let hoveringWatermark;

    hoveringWatermark = $("#hovering-watermark");
    hoveringWatermark.on("mousedown", function (event) {
        isDragging = true;
        offsetX = event.clientX - parseInt(hoveringWatermark.css("left"));
        offsetY = event.clientY - parseInt(hoveringWatermark.css("top"));
    });

    $(document).on("mousemove", function (event) {
        if (isDragging) {
            let x = event.clientX - offsetX;
            let y = event.clientY - offsetY;

            let imageContainer = $("#watermarked-image");
            let maxX = imageContainer.width() - hoveringWatermark.width();
            let maxY = imageContainer.height() - hoveringWatermark.height();

            x = Math.min(Math.max(x, 0), maxX);
            y = Math.min(Math.max(y, 0), maxY);

            hoveringWatermark.css({ left: x, top: y });

            $("#watermark-x").val(x);
            $("#watermark-y").val(y);
        }
    });

    $(document).on("mouseup", function () {
        isDragging = false;
    });

    $("#save-button").on("click", function () {
        let watermarkX = $("#watermark-x").val();
        let watermarkY = $("#watermark-y").val();

        let watermarkImage = $("#watermarked-image");
        let image = new Image();
        image.src = watermarkImage.attr("src");

        image.onload = function () {
            let canvas = document.createElement("canvas");
            canvas.width = image.width;
            canvas.height = image.height;
            canvas.style.position = "absolute";
            canvas.style.left = watermarkImage.position().left + "px";
            canvas.style.top = watermarkImage.position().top + "px";

            let context = canvas.getContext("2d");
            context.drawImage(image, 0, 0);

            context.font = "12px Arial";
            context.fillStyle = $("#text-color").val();
            context.fillText($("#watermark-text").val(), watermarkX, watermarkY);

            let link = document.createElement("a");
            link.href = canvas.toDataURL("image/png");
            link.download = "watermarked_image.png";
            link.click();
        };
    });
});
