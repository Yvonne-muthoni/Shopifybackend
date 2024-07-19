from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db, User, Order, Product, Payment

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route("/")
def index():
    return "<h1>Welcome to the Shopify</h1>"

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        print("Fetching all users...")
        users = User.query.all()
        users_dict = [user.to_dict() for user in users]
        print(f"Found {len(users_dict)} users.")
        return jsonify(users_dict), 200

    elif request.method == 'POST':
        print("Creating a new user...")
        data = request.json
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"User created: {new_user.to_dict()}")
        return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    print(f"Fetching user with ID {id}...")
    user = User.query.get(id)
    if user:
        print(f"User found: {user.to_dict()}")
        return jsonify(user.to_dict()), 200
    else:
        print(f"User with ID {id} not found.")
        return jsonify({'message': 'User not found'}), 404

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        print("Fetching all orders...")
        orders = Order.query.all()
        orders_dict = [order.to_dict() for order in orders]
        print(f"Found {len(orders_dict)} orders.")
        return jsonify(orders_dict), 200

    elif request.method == 'POST':
        print("Creating a new order...")
        data = request.json
        new_order = Order(
            user_id=data['user_id'],
            shipping_name=data['shipping_name'],
            shipping_address=data['shipping_address'],
            shipping_city=data['shipping_city'],
            shipping_state=data['shipping_state'],
            shipping_zip=data['shipping_zip'],
            billing_name=data['billing_name'],
            billing_address=data['billing_address'],
            billing_city=data['billing_city'],
            billing_state=data['billing_state'],
            billing_zip=data['billing_zip']
        )
        db.session.add(new_order)
        db.session.commit()
        print(f"Order created: {new_order.to_dict()}")
        return jsonify(new_order.to_dict()), 201

@app.route('/orders/<int:id>', methods=['GET'])
def get_order_by_id(id):
    print(f"Fetching order with ID {id}...")
    order = Order.query.get(id)
    if order:
        print(f"Order found: {order.to_dict()}")
        return jsonify(order.to_dict()), 200
    else:
        print(f"Order with ID {id} not found.")
        return jsonify({'message': 'Order not found'}), 404

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        print("Fetching all products...")
        products = Product.query.all()
        products_dict = [product.to_dict() for product in products]
        print(f"Found {len(products_dict)} products.")
        return jsonify(products_dict), 200

    elif request.method == 'POST':
        print("Creating a new product...")
        data = request.json
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price']
        )
        db.session.add(new_product)
        db.session.commit()
        print(f"Product created: {new_product.to_dict()}")
        return jsonify(new_product.to_dict()), 201

@app.route('/products/<int:id>', methods=['GET'])
def get_product_by_id(id):
    print(f"Fetching product with ID {id}...")
    product = Product.query.get(id)
    if product:
        print(f"Product found: {product.to_dict()}")
        return jsonify(product.to_dict()), 200
    else:
        print(f"Product with ID {id} not found.")
        return jsonify({'message': 'Product not found'}), 404

@app.route('/payments', methods=['GET', 'POST'])
def payments():
    if request.method == 'GET':
        print("Fetching all payments...")
        payments = Payment.query.all()
        payments_dict = [payment.to_dict() for payment in payments]
        print(f"Found {len(payments_dict)} payments.")
        return jsonify(payments_dict), 200

    elif request.method == 'POST':
        print("Creating a new payment...")
        data = request.json
        new_payment = Payment(
            order_id=data['order_id'],
            card_number=data['card_number'],
            expiration=data['expiration'],
            cvv=data['cvv']
        )
        db.session.add(new_payment)
        db.session.commit()
        print(f"Payment created: {new_payment.to_dict()}")
        return jsonify(new_payment.to_dict()), 201

@app.route('/payments/<int:id>', methods=['GET'])
def get_payment_by_id(id):
    print(f"Fetching payment with ID {id}...")
    payment = Payment.query.get(id)
    if payment:
        print(f"Payment found: {payment.to_dict()}")
        return jsonify(payment.to_dict()), 200
    else:
        print(f"Payment with ID {id} not found.")
        return jsonify({'message': 'Payment not found'}), 404

if __name__ == "__main__":
    app.run(port=5555, debug=True)
