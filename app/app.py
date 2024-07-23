import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5173"}}, supports_credentials=True)

    api = Api(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(128), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        def set_password(self, password):
            self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        def check_password(self, password):
            return bcrypt.check_password_hash(self.password_hash, password)

    class Product(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(120), nullable=False)
        price = db.Column(db.Float, nullable=False)
        image = db.Column(db.String(500), nullable=False)
        description = db.Column(db.String(500), nullable=True)  

    class Cart(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        items = db.relationship('CartItem', backref='cart', lazy=True)

    class CartItem(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
        cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
        quantity = db.Column(db.Integer, nullable=False, default=1)
        product = db.relationship('Product')

    productsFields = {
        'id': fields.Integer,
        'title': fields.String,
        'price': fields.Float,
        'image': fields.String,
        'description': fields.String  
    }

    cartItemFields = {
        'id': fields.Integer,
        'product': fields.Nested(productsFields),
        'quantity': fields.Integer
    }

    cartFields = {
        'id': fields.Integer,
        'items': fields.List(fields.Nested(cartItemFields))
    }

    class Products(Resource):
        @marshal_with(productsFields)
        def get(self):
            products = Product.query.all()
            return products

        @marshal_with(productsFields)
        def post(self):
            data = request.get_json()
            if isinstance(data, list):
                products = []
                for item in data:
                    new_product = Product(
                        title=item['title'],
                        price=item['price'],
                        image=item['image'],
                        description=item.get('description', '')  
                    )
                    db.session.add(new_product)
                    db.session.commit()
                    products.append(new_product)
                return products, 201
            else:
                new_product = Product(
                    title=data['title'],
                    price=data['price'],
                    image=data['image'],
                    description=data.get('description', '')  
                )
                db.session.add(new_product)
                db.session.commit()
                return new_product, 201

        @marshal_with(productsFields)
        def put(self, id):
            data = request.get_json()
            product = Product.query.get_or_404(id)

            product.title = data['title']
            product.price = data['price']
            product.image = data['image']
            product.description = data.get('description', '')  

            db.session.commit()
            return product, 200

        def delete(self, id):
            product = Product.query.get_or_404(id)
            db.session.delete(product)
            db.session.commit()
            return '', 204

    api.add_resource(Products, '/products', '/products/<int:id>')

    class CartResource(Resource):
        @marshal_with(cartFields)
        def get(self, id):
            cart = Cart.query.get_or_404(id)
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            cart.items = cart_items
            return cart

        @marshal_with(cartFields)
        def post(self, id):
            data = request.get_json()
            cart = Cart.query.get_or_404(id)

            product = Product.query.get_or_404(data['product_id'])
            existing_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()

            if existing_item:
                existing_item.quantity += data['quantity']
            else:
                new_item = CartItem(
                    product_id=product.id,
                    cart_id=cart.id,
                    quantity=data['quantity']
                )
                db.session.add(new_item)

            db.session.commit()
            return cart, 201

    api.add_resource(CartResource, '/carts/<int:id>')

    class CreateCartResource(Resource):
        def post(self):
            new_cart = Cart()
            db.session.add(new_cart)
            db.session.commit()
            return {'cart_id': new_cart.id}, 201

    api.add_resource(CreateCartResource, '/carts')

    @app.route('/register', methods=['POST', 'OPTIONS'])
    def register():
        if request.method == 'OPTIONS':
            return jsonify({}), 200  

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first() is not None:
            return jsonify(message='Email already registered'), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify(message='User registered successfully'), 201

    @app.route('/login', methods=['POST', 'OPTIONS'])
    def login():
        if request.method == 'OPTIONS':
            return jsonify({}), 200  

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return jsonify(message='Invalid credentials'), 401

        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5555)
