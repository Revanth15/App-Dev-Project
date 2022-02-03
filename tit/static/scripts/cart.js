$(document).ready (function() {
    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for (var i = 0; i < quantityInputs.length; i++) {
        var input = quantityInputs[i]
        input.addEventListener('change', quantityChanged)
    }

    var addToCartButtons = document.getElementsByClassName('shop-item-button')
    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var subtotal = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('S$', ''))
        var quantity = quantityElement.value
        total = price * quantity
        subtotal = subtotal + (price * quantity)

        cartRow.getElementsByClassName('cart-total')[0].innerText = 'S$' + total
    }
    // subtotal = Math.round(subtotal * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = 'S$' + subtotal


})

function addtocartClicked(element) {
    var item = element.value;
    $.post("/transactions/cart",
    {
        sku: item
    })
}


function quantityChanged(event) {
    var input = event.target
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateCartTotal()
}


function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var subtotal = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('S$', ''))
        var quantity = quantityElement.value
        total = price * quantity
        subtotal = subtotal + (price * quantity)

        cartRow.getElementsByClassName('cart-total')[0].innerText = 'S$' + total
    }
    // subtotal = Math.round(subtotal * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = 'S$' + subtotal
}

$('.cart-quantity-input').change(function() {
    var sku = $(this).parent('div').next().find("form").attr('action').split('/')[3]
    var quantity = $(this).val()

    $.getJSON('/transactions/update_cart', {
        sku: sku,
        quantity : quantity
      })
}) 

function wishList(wishlist) {
    wishlist.classList.toggle("bxs-heart")
}