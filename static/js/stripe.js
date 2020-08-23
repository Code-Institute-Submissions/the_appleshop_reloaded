function showCardErrorPopup() {
    $('#card-error-popup').css("transform", "translateZ(400px)").css("z-index", "400");
    setTimeout(function () {
        $('#card-error-popup').css("opacity", "1.0");
    }, 300);
}

function closeCardErrorPopup() {
    $('#card-error-popup').css("opacity", "0.0");
    setTimeout(function () {
        $('card-error-popup-message').html(``);
        $('#card-error-popup').css("transform", "translateZ(-10px)").css("z-index", "-1");
    }, 700);
}


$(function() {
    $("#payment-form").submit(function() {
        var form = this;
        var card = {
            number: $("#id_credit_card_number").val(),
            expMonth: $("#id_expiry_month").val(),
            expYear: $("#id_expiry_year").val(),
            cvc: $("#id_cvv").val()
        };
    
    Stripe.createToken(card, function(status, response) {
        if (status === 200) {
            $("#credit-card-errors").hide();
            $("#id_stripe_id").val(response.id);
            // Prevent the credit card details from being submitted
            // to our server
            $("#id_credit_card_number").removeAttr('name');
            $("#id_cvv").removeAttr('name');
            $("#id_expiry_month").removeAttr('name');
            $("#id_expiry_year").removeAttr('name');

            form.submit();
        } else {
            $("#stripe-error-message").text(response.error.message);
            $('#card-error-popup-message').html(response.error.message);
            $("#credit-card-errors").show();
            showCardErrorPopup();
            $("#validate_card_btn").attr("disabled", false);
        }
    });
    return false;
    });
});