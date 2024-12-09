from flask import render_template, request, redirect, url_for, flash, session, make_response, abort
from app import app, db
from app.models import User, Product, CartItem, Order, OrderItem, WishlistItem
from flask_login import login_user, logout_user, login_required, current_user, user_logged_in, user_logged_out
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import json

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Tea-Time Cakes Page
@app.route('/cakes')
def cakes():
    sort_option = request.args.get('sort')
    query = request.args.get('query', '').strip().lower()

    # Start with the base query filtering by category
    cakes_query = Product.query.filter_by(category='Cake')

    # Apply search filter based on the query
    if query:
        cakes_query = cakes_query.filter(Product.name.ilike(f'%{query}%'))

    # Apply sorting based on user selection
    if sort_option == 'lowest_to_highest':
        cakes_query = cakes_query.order_by(Product.price.asc())
    elif sort_option == 'highest_to_lowest':
        cakes_query = cakes_query.order_by(Product.price.desc())
    elif sort_option == 'A_to_Z':
        cakes_query = cakes_query.order_by(Product.name.asc())

    # Fetch the results after applying all filters and sorting
    cakes = cakes_query.all()

    return render_template('cakes.html', products=cakes, query=query)

# Cookies Page
@app.route('/cookies')
def cookies():
    sort_option = request.args.get('sort')
    query = request.args.get('query', '').strip().lower()

    # Start with the base query filtering by category
    cookies_query = Product.query.filter_by(category='Cookie')

    # Apply search filter based on the query
    if query:
        cookies_query = cookies_query.filter(Product.name.ilike(f'%{query}%'))

    # Apply sorting based on user selection
    if sort_option == 'lowest_to_highest':
        cookies_query = cookies_query.order_by(Product.price.asc())
    elif sort_option == 'highest_to_lowest':
        cookies_query = cookies_query.order_by(Product.price.desc())
    elif sort_option == 'A_to_Z':
        cookies_query = cookies_query.order_by(Product.name.asc())

    # Fetch the results after applying all filters and sorting
    cookies = cookies_query.all()

    return render_template('cookies.html', products=cookies, query=query)

# Chocolates Page
@app.route('/chocolates')
def chocolates():
    sort_option = request.args.get('sort')
    query = request.args.get('query', '').strip().lower()

    # Start with the base query filtering by category
    chocolates_query = Product.query.filter_by(category='Chocolate')

    # Apply search filter based on the query
    if query:
        chocolates_query = chocolates_query.filter(Product.name.ilike(f'%{query}%'))

    # Apply sorting based on user selection
    if sort_option == 'lowest_to_highest':
        chocolates_query = chocolates_query.order_by(Product.price.asc())
    elif sort_option == 'highest_to_lowest':
        chocolates_query = chocolates_query.order_by(Product.price.desc())
    elif sort_option == 'A_to_Z':
        chocolates_query = chocolates_query.order_by(Product.name.asc())

    # Fetch the results after applying all filters and sorting
    chocolates = chocolates_query.all()

    return render_template('chocolates.html', products=chocolates, query=query)

# Indian Desserts Page
@app.route('/indian-desserts')
def indian_desserts():
    sort_option = request.args.get('sort')
    query = request.args.get('query', '').strip().lower()

    # Start with the base query filtering by category
    desserts_query = Product.query.filter_by(category='Dessert')

    # Apply search filter based on the query
    if query:
        desserts_query = desserts_query.filter(Product.name.ilike(f'%{query}%'))

    # Apply sorting based on user selection
    if sort_option == 'lowest_to_highest':
        desserts_query = desserts_query.order_by(Product.price.asc())
    elif sort_option == 'highest_to_lowest':
        desserts_query = desserts_query.order_by(Product.price.desc())
    elif sort_option == 'A_to_Z':
        desserts_query = desserts_query.order_by(Product.name.asc())

    # Fetch the results after applying all filters and sorting
    desserts = desserts_query.all()

    return render_template('indian-desserts.html', products=desserts, query=query)

# Search Page for Items
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()

    if query:
        # Fetch all products matching the query across all categories
        search_results = Product.query.filter(Product.name.ilike(f'%{query}%')).all()

        if search_results:
            return render_template('search-items.html', products=search_results, query=query)

        # If no products are found, show a flash message and redirect
        flash(f"No results found for '{query}'. Please try again.", "warning")
        return redirect(url_for('home'))

    # Redirect to home if no query provided
    flash("Please enter a search term.", "info")
    return redirect(url_for('home'))

# Updating stock on purchase
def process_order(cart_items):
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if not product:
            abort(404, description="Product not found")
        try:
            product.update_stock(cart_item.quantity)
        except ValueError as e:
            abort(400, description=str(e))
    db.session.commit()

# Sign-Up Page for new customers
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists.", "danger")
            return render_template('signup.html')

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('signup.html')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # Create a new user
        new_user = User(
            name=name, 
            email=email, 
            password=hashed_password
        )
        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Automatically log in the new user
        login_user(new_user)
        flash("Account created and logged in successfully!", "success")
        return redirect(url_for('dashboard'))  # Redirect to the dashboard directly
    return render_template('signup.html')

# Login Page for existing customers
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Authenticate user
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html')

# Logout from their account 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# User dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user)

# Account updating for users
@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    new_email = request.form['newEmail']
    new_password = request.form['newPassword']
    confirm_password = request.form['confirmPassword']

    # Update email
    if new_email and new_email != current_user.email:
        current_user.email = new_email

    # Update password if new password is provided
    if new_password and new_password == confirm_password:
        hashed_password = generate_password_hash(new_password)  # Assuming you are hashing passwords
        current_user.password = hashed_password

    db.session.commit()
    flash("Account information updated successfully!", 'success')
    return redirect(url_for('dashboard'))

# Deleting the account deletes complete info about the user in database
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Delete user-related data from the database
    try:
        # Delete cart items (if any)
        CartItem.query.filter_by(user_id=current_user.id).delete()
        # Delete order items related to the user
        orders = Order.query.filter_by(user_id=current_user.id).all()
        for order in orders:
            OrderItem.query.filter_by(order_id=order.id).delete()
        # You can add code to delete other related user data (e.g., orders, reviews, etc.)
        # Now, delete the user
        user = User.query.get(current_user.id)
        db.session.delete(user)
        db.session.commit()

        # Log the user out
        logout_user()

        # Flash message and redirect
        flash("Your account has been deleted successfully.", 'success')
        return redirect(url_for('home'))  # Or redirect to a custom page

    except Exception as e:
        flash("There was an issue deleting your account. Please try again.", 'danger')
        return redirect(url_for('dashboard'))  # Or wherever the user was before

@app.route('/delete_order/<int:order_id>')
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id == current_user.id:
        db.session.delete(order)
        db.session.commit()
        flash('Your order has been deleted.', 'success')
    else:
        flash('You do not have permission to delete this order.', 'danger')
    
    return redirect(url_for('dashboard'))

# Cart functionalities
@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = {}

# Adding items to cart
@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))

    if not product_id:
        flash('Invalid product ID!', 'danger')
        return redirect(request.referrer or url_for('home'))

    product = Product.query.get(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(request.referrer or url_for('home'))
    
    # To check if the product is out of stock
    if product.stock < quantity:
        flash(f"{product.name}(s) not available. Out of stock.", 'danger')
        return redirect(request.referrer or url_for('home'))

    if current_user.is_authenticated:
        # For logged in users the cart is stored in the database
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if cart_item:
            total_quantity = cart_item.quantity + quantity
            if total_quantity > product.stock:
                flash(f"Cannot add more than {product.stock} {product.name} (Out of stock)", 'danger')
            else:
                cart_item.quantity = total_quantity
                db.session.commit()
                flash(f"{product.name} added to your cart!", 'success')
        else:
            new_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
            db.session.add(new_item)
            db.session.commit()
            flash(f"{product.name} added to your cart!", 'success')
    else:
        # For unauthenticated user or logged out users the cart is stored in session
        cart = session.get('cart', {})
        if product_id in cart:
            total_quantity = cart[product_id]['quantity'] + quantity
            if total_quantity > product.stock:
                flash(f"Cannot add more than {product.stock} {product.name} (Out of stock)", 'danger')
            else:
                cart[product_id]['quantity'] = total_quantity
                flash(f"{product.name} added to your cart!", 'success')
        else:
            cart[product_id] = {
                'name': product.name,
                'price': product.price,
                'image': product.image,
                'quantity': quantity,
                'stock': product.stock  
            }
            flash(f"{product.name} added to your cart!", 'success')

        # Save the updated cart in the session
        session['cart'] = cart
        session.modified = True

    return redirect(request.referrer or url_for('home'))

@app.route('/update-cart', methods=['POST'])
def update_cart():
    data = request.get_json()
    item_id = str(data.get('itemId'))  # Always handle item_id as a string for session consistency
    change = int(data.get('change'))  # +1 for increment, -1 for decrement

    if current_user.is_authenticated:
        # For authenticated users
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=item_id).first()
        if not cart_item:
            return jsonify({'status': 'error', 'message': 'Item not found in cart'}), 404

        new_quantity = cart_item.quantity + change

        if new_quantity < 1:
            # Remove item from cart if quantity drops to 0
            db.session.delete(cart_item)
        elif new_quantity > cart_item.product.stock:
            return jsonify({'status': 'error', 'message': f'Only {cart_item.product.stock} {cart_item.product.name}(s) available'}), 400
        else:
            cart_item.quantity = new_quantity

        db.session.commit()

        # Calculate totals
        cart_total = sum([ci.product.price * ci.quantity for ci in CartItem.query.filter_by(user_id=current_user.id).all()])
        item_total = cart_item.product.price * cart_item.quantity

    else:
        # For unauthenticated users
        cart = session.get('cart', {})
        if item_id not in cart:
            return jsonify({'status': 'error', 'message': 'Item not found in cart'}), 404

        item = cart[item_id]
        new_quantity = item['quantity'] + change

        if new_quantity < 1:
            # Remove item from cart if quantity drops to 0
            del cart[item_id]
        elif new_quantity > item.get('stock', 10):  # Default stock to 10 if not specified
            return jsonify({'status': 'error', 'message': f'Only {item["stock"]} {item["name"]}(s) available'}), 400
        else:
            item['quantity'] = new_quantity

        session['cart'] = cart
        session.modified = True

        # Calculate totals
        cart_total = sum([v['price'] * v['quantity'] for v in cart.values()])
        item_total = item['price'] * item['quantity']

    return jsonify({
        'status': 'success',
        'newQuantity': new_quantity,
        'itemTotal': item_total,
        'cartTotal': cart_total
    })


# Deleting items from cart
@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    # For logged-in users
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=item_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
    
    # For unauthenticated users
    else:
        cart = session.get('cart', {})
        if str(item_id) in cart: 
            del cart[str(item_id)] 
        session['cart'] = cart
        session.modified = True 
    flash("Item Removed!", 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/cart')
def view_cart():
    if current_user.is_authenticated:
        # Fetch cart items from the database for logged-in users
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart = [{
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'stock': item.product.stock,
            'image': item.product.image
        } for item in cart_items]

        # Stock validation: Adjust quantity if it exceeds available stock
        for item in cart:
            if item['quantity'] > item['stock']:
                # Adjust quantity to available stock
                item['quantity'] = item['stock']
                flash(f"Insufficient stock for {item['name']}. Quantity has been adjusted to {item['stock']}.", "danger")

    else:
        # Fetch cart from session for unauthenticated users
        cart = session.get('cart', {})
        cart = [{
            'id': pid,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'stock': item['stock'],
            'image': item['image']
        } for pid, item in cart.items()]

        # Stock validation: Adjust quantity if it exceeds available stock
        for item in cart:
            product = Product.query.get(item['id'])  # Get product to check stock
            if item['quantity'] > product.stock:
                # Adjust quantity to available stock
                item['quantity'] = product.stock
                flash(f"Insufficient stock for {item['name']}. Quantity has been adjusted to {product.stock}.", "danger")
    
    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    return render_template('cart.html', cart=cart, total_price=total_price)

@user_logged_in.connect_via(app)
def merge_carts(sender, user):
    guest_cart = session.get('cart', {})
    
    if guest_cart:  # Proceed only if there is a session cart
        for product_id, details in guest_cart.items():
            # Fetch the product from the database
            product = Product.query.get(product_id)
            if not product:
                continue  # Skip if the product doesn't exist in the database

            cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product_id).first()

            # Check if stock is sufficient
            if product.stock < details['quantity']:
                flash(f"Insufficient stock for {product.name}. Only {product.stock} left.", "danger")
                # Adjust the quantity to the available stock if it exceeds
                details['quantity'] = product.stock  # Limit the quantity to available stock

            if cart_item:
                # Merge quantities for existing items
                cart_item.quantity += details['quantity']
            else:
                # Add new items from the session cart to the database cart
                new_item = CartItem(user_id=user.id, product_id=product_id, quantity=details['quantity'])
                db.session.add(new_item)

        db.session.commit()
    
    # Clear session cart after merging
    session.pop('cart', None)  
    session.modified = True


# Clearing the session cart once the items are saved in the database cart when logged in
@user_logged_out.connect_via(app)
def save_cart_on_logout(sender, user):
    print(f"User {user.id} logged out. Cart remains in the database.") 
    session.pop('cart', None) 
    session.modified = True

# Help from chatGPT on how to get the quantity of items in the cart
# Cart icon dynamically updates with the total quantity of items in the cart
@app.context_processor
def inject_cart_quantity():
    if current_user.is_authenticated:
        # Fetch the total quantity from the database cart for logged-in users
        total_quantity = db.session.query(
            db.func.sum(CartItem.quantity)
        ).filter_by(user_id=current_user.id).scalar() or 0
    else:
        # Fetch the total quantity from the session cart for unauthenticated users
        cart = session.get('cart', {})
        total_quantity = sum(item['quantity'] for item in cart.values())
    
    return dict(cart_total_quantity=total_quantity)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # Retrieve items in the cart
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    # Validate stock before proceeding (only for GET requests)
    if request.method == 'GET':
        insufficient_stock = [
            item for item in cart_items if item.product.stock < item.quantity
        ]
        
        # If there are any items with insufficient stock, adjust the quantity
        if insufficient_stock:
            for item in insufficient_stock:
                flash(f"Insufficient stock for {item.product.name}. Only {item.product.stock} left.", "danger")
                # Adjust the quantity to available stock
                item.quantity = item.product.stock
            db.session.commit()  # Save the changes to the cart

    if not cart_items:
        flash("Your cart is empty!", "danger")
        return redirect(url_for('cart'))

    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # If POST request, handle the checkout submission
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')

        if not name or not address:
            flash("Please fill in all the details.", "danger")
            return redirect(url_for('checkout'))

        try:
            # Create the order for the user (this can be a new Order model)
            order = Order(user_id=current_user.id, total_amount=total_amount, name=name, address=address)
            db.session.add(order)
            db.session.flush()  # This ensures the order has an ID before committing

            # Reduce the stock for each product in the cart
            for item in cart_items:
                item.product.update_stock(item.quantity)
                # Create an order item in the OrderItem table (you can create this model if needed)
                order_item = OrderItem(order_id=order.id, product_id=item.product.id, quantity=item.quantity)
                db.session.add(order_item)

            db.session.commit()

            # Clear the user's cart after order is placed
            CartItem.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()

            flash("Order placed successfully!", "success")
            return redirect(url_for('dashboard'))
        except ValueError as e:
            db.session.rollback()  # Rollback if any error occurs
            flash(str(e), "danger")
            return redirect(url_for('view_cart'))

    # Render the checkout page
    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/place_order', methods=['POST'])
def place_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    total_amount = 0
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product.stock < cart_item.quantity:
            flash('Insufficient stock for one or more products.', 'error')
            return redirect(url_for('view_cart'))

        total_amount += product.price * cart_item.quantity
        product.update_stock(cart_item.quantity)

    # Check if user has already placed an order
    existing_order = Order.query.filter_by(user_id=current_user.id).first()

    if existing_order:
        # Link the new order to the existing order if the user is a returning customer
        order = existing_order
        order.total_amount += total_amount  # Add the new total to the existing order total
    else:
        # Create a new order for new customers
        order = Order(user_id=current_user.id, total_amount=total_amount, name=current_user.name, address=request.form['address'])
        db.session.add(order)

    db.session.commit()

    # Create order items
    for cart_item in cart_items:
        order_item = OrderItem(order_id=order.id, product_id=cart_item.product_id, quantity=cart_item.quantity)
        db.session.add(order_item)

    db.session.commit()

    # Clear the user's cart after order
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return redirect(url_for('dashboard'))  # Redirect to the dashboard

@app.route('/product/details/<int:product_id>', methods=['GET'])
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'image': url_for('static', filename=product.image),
        'price': product.price
    })

# Route for guest checkout for unauthentiacted users
@app.route('/guest-checkout')
def guest_checkout():
    cart = session.get('cart', {})
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart'))  # Redirect to the cart page if empty

    # Logic to handle checkout for guest users (non-authenticated)
    return render_template('guest_checkout.html', cart=cart)

@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    if not current_user.is_authenticated:
        return jsonify({'status': 'not_logged_in'}), 401  # Return status for not logged-in user

    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'status': 'error', 'message': 'No product ID provided.'}), 400

    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'status': 'error', 'message': 'Product not found.'}), 404

    # Check if the product is already in the user's wishlist
    existing_item = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_item:
        return jsonify({'status': 'exists'})

    # Add the product to the wishlist
    new_item = WishlistItem(user_id=current_user.id, product_id=product_id)
    db.session.add(new_item)
    db.session.commit()

    # Fetch updated wishlist items
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    wishlist_data = [
        {
            'id': item.id,
            'product_name': item.product.name,
            'product_price': item.product.price,
            'product_image': url_for('static', filename=item.product.image)
        }
        for item in wishlist_items
    ]

    return jsonify({'status': 'success', 'wishlist': wishlist_data})

@app.route('/delete_from_wishlist', methods=['POST'])
@login_required
def delete_from_wishlist():
    data = request.get_json()
    item_id = data.get('item_id')

    # Check if the item exists
    wishlist_item = WishlistItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not wishlist_item:
        return jsonify({'status': 'error', 'message': 'Item not found.'}), 404

    # Remove the item from the wishlist
    db.session.delete(wishlist_item)
    db.session.commit()

    # Fetch updated wishlist items
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    wishlist_data = [
        {
            'id': item.id,
            'product_name': item.product.name,
            'product_price': item.product.price,
            'product_image': url_for('static', filename=item.product.image)
        }
        for item in wishlist_items
    ]

    return jsonify({'status': 'success', 'wishlist': wishlist_data})

@app.route('/get_wishlist', methods=['GET'])
@login_required
def get_wishlist():
    # Fetch the user's wishlist items
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    wishlist_data = [
        {
            'id': item.id,
            'product_name': item.product.name,
            'product_price': item.product.price,
            'product_image': url_for('static', filename=item.product.image)
        }
        for item in wishlist_items
    ]
    return jsonify({'status': 'success', 'wishlist': wishlist_data})




