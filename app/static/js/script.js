// https://blog.udemy.com/jquery-settimeout/ - Reference
// Automatically dismiss flash messages after 3 seconds
$(document).ready(function() {
setTimeout(function() {
    $(".alert").alert('close');
}, 3000); // 3000 milliseconds = 3 seconds
});

// Cookies settings for the website - Help from section_12 in the module website. 
window.addEventListener("load", function () {
    window.cookieconsent.initialise({
      "palette": {
        "popup": {
          "background": "#f4eeee", 
          "text": "#5c7291"
        },
        "button": {
          "background": "#f4eeee", 
          "text": "#5c7291" 
        }
      },
      "theme": "classic", 
      "position": "bottom",
      "content": {
        "message": "This website uses cookies to ensure you get the best experience.",
        "dismiss": "Accept all", 
        "link": "Learn more",
        "href": "#" 
      }
    });
  
    // Automatically remove the cookie banner once "Accept all" button is clicked - help from chatGPT 
    document.addEventListener("click", function (e) {
      if (e.target.classList.contains("cc-btn")) {
        const cookieBanner = document.querySelector(".cc-window");
        if (cookieBanner) {
          cookieBanner.style.display = "none"; 
        }
      }
    });
  });

// Increment and  decremnet of quanity of the items in the cart webpage
$(document).ready(function () {
    $("button.update-quantity").on("click", function () {
        const itemId = $(this).data("item-id"); // Get the item ID
        const change = parseInt($(this).data("change")); // +1 for increment, -1 for decrement

        // Send AJAX request to update quantity
        $.ajax({
            url: "/update-cart",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ itemId: itemId, change: change }),
            success: function (response) {
                if (response.status === "success") {
                    // Update the quantity and totals dynamically
                    $(`#quantity-${itemId}`).text(response.newQuantity);
                    $(`#total-${itemId}`).text(`£${response.itemTotal.toFixed(2)}`);
                    $("#cart-total").text(`Total: £${response.cartTotal.toFixed(2)}`);
                } else {
                    alert(response.message);
                }
            },
            error: function (xhr) {
                const response = JSON.parse(xhr.responseText);
                alert(response.message);
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Attach click event listeners to all like buttons
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productId = button.getAttribute('data-product-id');
            addToWishlist(productId);
        });
    });
});

// Adding item to wishlist
function addToWishlist(productId) {
    fetch('/add_to_wishlist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'not_logged_in') {
            alert('Please log in to add items to your wishlist.');
            window.location.href = '/login';  // Redirect to login page
        } else if (data.status === 'success') {
            alert('Item added to your wishlist!');
            updateWishlistModal(data.wishlist); // Update wishlist modal
            $('#wishlistModal').modal('show'); // Show the modal
        } else if (data.status === 'exists') {
            alert('Item is already in your wishlist!');
            updateWishlistModal(data.wishlist); // Update modal even if item exists
            $('#wishlistModal').modal('show'); // Show the modal
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    });
}

// Load wishlist when the modal is opened
$('#wishlistModal').on('show.bs.modal', function () {
    // Check if the user is logged in before fetching wishlist data
    fetch('/get_wishlist')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'not_logged_in') {
                alert('You need to log in to view your wishlist.');
                window.location.href = '/login';  // Redirect to login page
            } else if (data.status === 'success') {
                updateWishlistModal(data.wishlist);
            } else {
                alert('Failed to load wishlist. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        });
});

function updateWishlistModal(wishlist) {
    const wishlistContainer = document.getElementById('wishlist-items');
    wishlistContainer.innerHTML = ''; // Clear existing items

    if (wishlist.length === 0) {
        wishlistContainer.innerHTML = '<p class="text-center">Your wishlist is empty.</p>';
        return;
    }

    wishlist.forEach(item => {
        const wishlistItem = `
            <div class="wishlist-item d-flex align-items-center justify-content-between mb-2">
                <div class="d-flex align-items-center">
                    <img src="${item.product_image}" alt="${item.product_name}" class="wishlist-image" style="width: 50px; height: 50px; margin-right: 10px;">
                    <div>
                        <p class="mb-0">${item.product_name}</p>
                        <p class="mb-0">£${item.product_price}</p>
                    </div>
                </div>
                <!-- Delete button -->
                <a href="#" class="delete-btn" onclick="removeFromWishlist(${item.id})">
                    <i class="fa fa-trash text-danger" style="font-size: 1.2rem;"></i>
                </a>
            </div>
        `;
        wishlistContainer.insertAdjacentHTML('beforeend', wishlistItem);
    });
}

// Function to handle wishlist item deletion
function removeFromWishlist(itemId) {
    fetch('/delete_from_wishlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: itemId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Item removed from wishlist.');
            updateWishlistModal(data.wishlist); // Update modal content
        } else {
            alert('Failed to remove item. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    });
}