from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'orders': [order.to_dict() for order in self.orders]
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    orders = db.relationship('OrderItem', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'orders': [order.to_dict() for order in self.orders]
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    shipping_name = db.Column(db.String(128), nullable=False)
    shipping_address = db.Column(db.String(256), nullable=False)
    shipping_city = db.Column(db.String(64), nullable=False)
    shipping_state = db.Column(db.String(64), nullable=False)
    shipping_zip = db.Column(db.String(10), nullable=False)
    billing_name = db.Column(db.String(128), nullable=False)
    billing_address = db.Column(db.String(256), nullable=False)
    billing_city = db.Column(db.String(64), nullable=False)
    billing_state = db.Column(db.String(64), nullable=False)
    billing_zip = db.Column(db.String(10), nullable=False)
    payment = db.relationship('Payment', backref='order', uselist=False)

    def __repr__(self):
        return f'<Order {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'order_items': [item.to_dict() for item in self.order_items],
            'shipping_name': self.shipping_name,
            'shipping_address': self.shipping_address,
            'shipping_city': self.shipping_city,
            'shipping_state': self.shipping_state,
            'shipping_zip': self.shipping_zip,
            'billing_name': self.billing_name,
            'billing_address': self.billing_address,
            'billing_city': self.billing_city,
            'billing_state': self.billing_state,
            'billing_zip': self.billing_zip,
            'payment': self.payment.to_dict() if self.payment else None
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiration = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f'<Payment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'card_number': self.card_number,
            'expiration': self.expiration,
            'cvv': self.cvv
        }
