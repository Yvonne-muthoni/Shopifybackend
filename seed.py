from app import app, db
from models import User, Order, Product, Payment

def seed_data():
    with app.app_context():
       
        if not User.query.filter_by(username='john_doe').first():
            user1 = User(username='john_doe', email='john@example.com', password='password134')
            db.session.add(user1)
        else:
            user1 = User.query.filter_by(username='john_doe').first()
        
        if not User.query.filter_by(username='jane_smith').first():
            user2 = User(username='jane_smith', email='jane@example.com', password='password23')
            db.session.add(user2)
        else:
            user2 = User.query.filter_by(username='jane_smith').first()

      
        if not Product.query.filter_by(name='Product A').first():
            product1 = Product(name='Product A', price=19.99, description='Description for Product A')
            db.session.add(product1)
        else:
            product1 = Product.query.filter_by(name='Product A').first()

        if not Product.query.filter_by(name='Product B').first():
            product2 = Product(name='Product B', price=29.99, description='Description for Product B')
            db.session.add(product2)
        else:
            product2 = Product.query.filter_by(name='Product B').first()

       
        db.session.commit()

       
        order1 = Order(user_id=user1.id, product_id=product1.id, quantity=2, total=product1.price * 2)
        order2 = Order(user_id=user2.id, product_id=product2.id, quantity=1, total=product2.price)

       
        payment1 = Payment(amount=order1.total, currency='USD', status='paid')
        payment2 = Payment(amount=order2.total, currency='USD', status='pending')

      
        db.session.add(order1)
        db.session.add(order2)
        db.session.add(payment1)
        db.session.add(payment2)

        
        db.session.commit()

        print("Seeding completed successfully.")

if __name__ == '__main__':
    seed_data()
