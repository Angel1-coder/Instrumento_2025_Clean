/*
    Stripe Elements integration for secure payment processing
    Handles card validation and payment submission
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

// Initialize Stripe
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

// Custom styling for the card element
var style = {
    base: {
        color: '#32325d',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
    }
};

// Create and mount the card element
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle real-time validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
        // Add subtle shake animation for better UX
        $('#card-element').addClass('shake');
        setTimeout(function() {
            $('#card-element').removeClass('shake');
        }, 500);
    } else {
        errorDiv.textContent = '';
        // Clear any previous error styling
        $('#card-element').removeClass('shake');
    }
});

// Handle form submission
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    
    // Disable form submission to prevent double submission
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    
    // Show loading overlay
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    
    // Get CSRF token from the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    
    // Cache checkout data before payment confirmation
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
        // Confirm card payment with Stripe
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            }
        }).then(function(result) {
            if (result.error) {
                // Payment failed - show error message
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>
                `;
                $(errorDiv).html(html);
                
                // Re-enable form
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
                
                // Scroll to error
                $('html, body').animate({
                    scrollTop: $('#card-errors').offset().top - 100
                }, 500);
            } else {
                // Payment successful - submit the form
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function() {
        // Cache checkout data failed
        var errorDiv = document.getElementById('card-errors');
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>Failed to process payment. Please try again.</span>
        `;
        $(errorDiv).html(html);
        
        // Re-enable form
        $('#payment-form').fadeToggle(100);
        $('#loading-overlay').fadeToggle(100);
        card.update({ 'disabled': false});
        $('#submit-button').attr('disabled', false);
    });
});