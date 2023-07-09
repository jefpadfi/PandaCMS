$(document).ready(function () {
    // Initialize the carousel
    $("#slider").carousel();

    // Enable swipe gesture for touch devices
    $("#slider").on("touchstart", function (event) {
        var xClick = event.originalEvent.touches[0].pageX;
        $(this).one("touchmove", function (event) {
            var xMove = event.originalEvent.touches[0].pageX;
            if (Math.floor(xClick - xMove) > 5) {
                $(this).carousel("next");
            } else if (Math.floor(xClick - xMove) < -5) {
                $(this).carousel("prev");
            }
        });
        $(this).on("touchend", function () {
            $(this).off("touchmove");
        });
    });
});