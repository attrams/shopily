$(document).ready(function () {
  /*  ---------------------------------------------------
    Template Name: Ogani
    Description:  Ogani eCommerce  HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

  ('use strict');

  (function ($) {
    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
      var bg = $(this).data('setbg');
      $(this).css('background-image', 'url(' + bg + ')');
    });

    //Humberger Menu
    $('.humberger__open').on('click', function () {
      $('.humberger__menu__wrapper').addClass('show__humberger__menu__wrapper');
      $('.humberger__menu__overlay').addClass('active');
      $('body').addClass('over_hid');
    });

    $('.humberger__menu__overlay').on('click', function () {
      $('.humberger__menu__wrapper').removeClass(
        'show__humberger__menu__wrapper'
      );
      $('.humberger__menu__overlay').removeClass('active');
      $('body').removeClass('over_hid');
    });

    /*------------------
		Navigation
	--------------------*/
    $('.mobile-menu').slicknav({
      prependTo: '#mobile-menu-wrap',
      allowParentLinks: true,
    });

    /*--------------------------
        Select
    ----------------------------*/
    $('select').niceSelect();

    /*------------------
		Single Product
	--------------------*/
    $('.product__details__pic__slider img').on('click', function () {
      var imgurl = $(this).data('imgbigurl');
      var bigImg = $('.product__details__pic__item--large').attr('src');
      if (imgurl != bigImg) {
        $('.product__details__pic__item--large').attr({
          src: imgurl,
        });
      }
    });

    /*-------------------
		Quantity change
	--------------------- */
    var proQty = $('.pro-qty');
    proQty.prepend('<span class="dec qtybtn">-</span>');
    proQty.append('<span class="inc qtybtn">+</span>');
    proQty.on('click', '.qtybtn', function () {
      var $button = $(this);
      var oldValue = $button.parent().find('input').val();
      var minVal = parseInt($button.parent().find('input').attr('min'));
      var maxVal = parseInt($button.parent().find('input').attr('max'));

      if ($button.hasClass('inc')) {
        // max quantity value
        if (oldValue < maxVal) {
          var newVal = parseFloat(oldValue) + 1;
        } else {
          newVal = oldValue;
        }
      } else {
        // Don't allow decrementing below zero
        if (oldValue > minVal) {
          var newVal = parseFloat(oldValue) - 1;
        } else {
          newVal = 1;
        }
      }
      $button.parent().find('input').val(newVal);

      // manually trigger change to allow the total price updating function to work
      $button.parent().find('input').trigger('change');
    });

    /* -----------------------
    Modal Autofocus
  -------------------------- */
    $('#modalCenter').on('shown.bs.modal', function () {
      $('#modalInputContent').trigger('focus');
    });

    /* -----------------------
    Modal Reset
  -------------------------- */
    $('#modalCenter').on('hidden.bs.modal', function () {
      // clear input field when closed
      $('#modalInputContent').val('');
    });

    /* ---------------------------
    Modal Apply button pressed
  ------------------------------ */
    $('.modal-footer .btn-apply').click(function () {
      // Get the value from the input field
      var couponCode = $('#modalInputContent').val();

      if (couponCode) {
        const csrftoken = Cookies.get('csrftoken');
        var url = '/coupons/apply/';

        var options = {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
          },
          mode: 'same-origin',
        };

        var formData = new FormData();
        formData.append('code', couponCode);
        options['body'] = formData;

        // send HTTP request
        fetch(url, options)
          .then((response) => response.json())
          .then((data) => {
            if (data['redirect']) {
              window.location.href = data['redirect_url'];
            }
            // Optionally close the modal after applying the coupon
            $('#modalCenter').modal('hide');
          });
      }
    });

    /*----------------------------
    Add to Cart
  ------------------------------ */
    $('#add-to-cart-btn').click(function (e) {
      e.preventDefault();

      const csrftoken = Cookies.get('csrftoken');
      var quantity = $('#quantity-input').val()
        ? $('#quantity-input').val()
        : 1;
      var product_id = $(this).data('product-id');
      var override = false;

      var url = `/cart/add/${product_id}/`;

      var options = {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest',
        },
        mode: 'same-origin',
      };

      // add request body
      var formData = new FormData();
      formData.append('quantity', quantity);
      formData.append('override', override);
      options['body'] = formData;

      // send HTTP request
      fetch(url, options)
        .then((response) => response.json())
        .then((data) => {
          if (data['redirect']) {
            window.location.href = data['redirect_url'];
          }
        });
    });

    /*-------------------------------
    Update Quantity in Cart Detail
  --------------------------------- */
    $('.pro-qty').on('change', 'input', function (e) {
      var productId = $(this).data('product-id');

      if (productId) {
        var newQuantity = $(this).val();
        var updateUrl = `/cart/update/${productId}/`;

        const csrftoken = Cookies.get('csrftoken');

        var options = {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
          },
          mode: 'same-origin',
          body: JSON.stringify({
            quantity: `${newQuantity}`,
          }),
        };

        fetch(updateUrl, options)
          .then((response) => response.json())
          .then((data) => {
            if (data['success']) {
              // update total item count in the header
              $('.total-items').text(data['cartTotalItems']);

              // update the total in the header
              $('.total-price').text(`$${data['cartTotalPrice']}`);

              // update the item total price
              $('#item-total-price-' + productId).text(
                `$${data['updatedItemTotalPrice']}`
              );

              // update subtotal
              $('#cart-subtotal').text(`$${data['cartSubtotalPrice']}`);

              // update discount
              $('#cart-discount').text(`- $${data['cartDiscount']}`);

              // update total
              $('#cart-total').text(`$${data['cartTotalPrice']}`);
            }
          });
      }
    });

    /* ----------------------------
       Toggle password visibility
       ---------------------------- */
    $('#togglePassword').click(function () {
      const password = $('#password');
      const type = password.attr('type') === 'password' ? 'text' : 'password';
      password.attr('type', type);

      // toggle the eye/eye-slash icon
      $(this).toggleClass('fa-eye fa-eye-slash');
    });

    /* ---------------------------------------------------------
        Hide login input errors when user starts typing
       --------------------------------------------------------- */

    $('#user-login input').on('input', function () {
      // Find the closest parent container (e.g., '.form-group') and search for the '.error' within it and hide
      $(this).closest('.form-group').find('.error').hide();
    });
  })(jQuery);
});
