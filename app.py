from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)
api = Api(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    orders = db.relationship('Order', secondary='order_product')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    products = db.relationship('Product', secondary='order_product')

order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

productsFields = {
    'id': fields.Integer,
    'title': fields.String,
    'price': fields.Float,
    'image': fields.String
}

class Products(Resource):
    @marshal_with(productsFields)
    def get(self):
        products = Product.query.all()
        return products
    
    @marshal_with(productsFields)
    def post(self):
        data = request.get_json()
        new_product = Product(
            title=data['title'],
            price=data['price'],
            image=data['image']
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
        
        db.session.commit()
        return product, 200

    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

class Orders(Resource):
    def get(self):
        orders = Order.query.all()
        return orders
    
    def post(self):
        data = request.get_json()
        customer_name = data.get('customer_name')
        product_ids = data.get('product_ids', [])

        new_order = Order(customer_name=customer_name)
        for product_id in product_ids:
            product = Product.query.get_or_404(product_id)
            new_order.products.append(product)

        db.session.add(new_order)
        db.session.commit()
        return new_order.id, 201


api.add_resource(Products, '/products', '/products/<int:id>')
api.add_resource(Orders, '/orders', '/orders/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
