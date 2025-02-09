// ✅ Get CSRF token only once and store globally
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ✅ Declare 'csrftoken' globally if not already set
if (typeof window.csrftoken === "undefined") {
    window.csrftoken = getCookie('csrftoken');
}

// ✅ Function to get and validate cart from cookies
function getCart() {
    let cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
        let parts = cookies[i].split("=");
        if (parts[0] === "cart") {
            try {
                return JSON.parse(decodeURIComponent(parts[1]));
            } catch (error) {
                console.error("Cart cookie is invalid, resetting cart:", error);
                document.cookie = "cart={}; path=/";
                return {}; // Reset cart
            }
        }
    }
    return {}; // Return empty cart if not found
}

// ✅ Declare 'cart' only once
if (typeof window.cart === "undefined") {
    window.cart = getCart();
}

// ✅ Event listener for cart update buttons
document.querySelectorAll(".update-cart").forEach(button => {
    button.addEventListener("click", function () {
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log("Product ID:", productId, "Action:", action);

        if (typeof user !== "undefined" && user === "AnonymousUser") {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
});

// ✅ Function to handle cart for anonymous users (store in cookies)
function addCookieItem(productId, action) {
    console.log('User not logged in, saving to cookies...');

    if (action === 'add') {
        cart[productId] = cart[productId] ? { 'quantity': cart[productId].quantity + 1 } : { 'quantity': 1 };
    } else if (action === 'remove') {
        cart[productId].quantity -= 1;
        if (cart[productId].quantity <= 0) {
            delete cart[productId];
        }
    }

    console.log('Updated Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + "; path=/";
    location.reload();
}

// ✅ Function to update user cart in the database
function updateUserOrder(productId, action) {
    console.log("User is logged in, sending data...");
    fetch("/update_item/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrftoken,
        },
        body: JSON.stringify({ productId: productId, action: action }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
        location.reload();
    })
    .catch(error => {
        console.error("Fetch Error:", error);
        alert("Error updating cart. Please try again.");
    });
}

// ✅ Function to process order (checkout)
function processOrder() {
    fetch("/processOrder/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrftoken,
        },
        body: JSON.stringify({
            form: { total: document.getElementById("total-price").innerText }
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Payment successful:", data);
        window.location.href = "/order-success/";  // Redirect after success
    })
    .catch(error => {
        console.error("Error processing order:", error);
        alert("Error processing order. Please try again.");
    });
}
