from flask_login import UserMixin
from app import db
from datetime import datetime

# Table for the user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)  

    def __repr__(self):
        return f'<User {self.name}>'

# Table for each product available on the site
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'Cake', 'Cookie', 'Chocolate', 'Desserts'.
    image = db.Column(db.String(225), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)  # Stock quantity

    def update_stock(self, quantity):
        if self.stock - quantity < 0:
            raise ValueError("Insufficient stock.")
        self.stock -= quantity
    
    def __repr__(self):
        return f'<Product {self.name}>'

# Table to store cart items
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Link to Product table
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Relationships to fetch related data
    product = db.relationship('Product')  
    user = db.relationship('User', backref='cart_items')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)  # Changed from phone to address
    date_ordered = db.Column(db.Date, default=datetime.utcnow().date)  # Only storing the date (not datetime)

    user = db.relationship('User', backref='orders')
    order_items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')  # Ensure this cascade setting

# Table to store items in each order
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product')


# Table to store wishlist items
class WishlistItem(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # Link to Product table

    # Relationships to fetch related data
    product = db.relationship('Product')
    user = db.relationship('User', backref='wishlist_items')

    def __repr__(self):
        return f'<WishlistItem {self.user_id} - {self.product_id}>'