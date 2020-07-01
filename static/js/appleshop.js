$(document).ready(function () {

});

function showDeletePopup() {
    $('#confirmDeletePopup').css("transform", "translateZ(400px)").css("z-index", "400");
    setTimeout(function() {
        $('#confirmDeletePopup').css("opacity", "1.0");
    }, 300);
}

function closeDeletePopup(){
    $('#confirmDeletePopup').css("opacity", "0.0");
    setTimeout(function() {
        $('#confirmDeletePopup').css("transform", "translateZ(-10px)").css("z-index", "-1");
    }, 700);
}