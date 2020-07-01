$(document).ready(function () {

});

function showDeletePopup() {
    $('#confirm-delete-popup').css("transform", "translateZ(400px)").css("z-index", "400");
    setTimeout(function() {
        $('#confirm-delete-popup').css("opacity", "1.0");
    }, 300);
}

function closeDeletePopup(){
    $('#confirm-delete-popup').css("opacity", "0.0");
    setTimeout(function() {
        $('#confirm-delete-popup').css("transform", "translateZ(-10px)").css("z-index", "-1");
    }, 700);
}