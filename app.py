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
    return "<h1>Welcome to the Flask App</h1>"

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200

    elif request.method == 'POST':
        data = request.json
        new_user = User(
            username=data['username'],
            email=data['email']
           
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200

    elif request.method == 'POST':
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
        return jsonify(new_order.to_dict()), 201

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200

    elif request.method == 'POST':
        data = request.json
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201

@app.route('/payments', methods=['GET', 'POST'])
def payments():
    if request.method == 'GET':
        payments = Payment.query.all()
        return jsonify([payment.to_dict() for payment in payments]), 200

    elif request.method == 'POST':
        data = request.json
        new_payment = Payment(
            order_id=data['order_id'],
            card_number=data['card_number'],
            expiration=data['expiration'],
            cvv=data['cvv']
        )
        db.session.add(new_payment)
        db.session.commit()
        return jsonify(new_payment.to_dict()), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)
