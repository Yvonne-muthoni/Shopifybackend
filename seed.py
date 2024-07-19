from app import app, db
from models import User, Product, Order, OrderItem, Payment
import bcrypt

def seed():
    with app.app_context():
        
        db.drop_all()
        db.create_all()

       
        def hash_password(password):
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

      
        user1 = User(username='john_doe', email='john@example.com', password=hash_password('password123'))
        user2 = User(username='jane_doe', email='jane@example.com', password=hash_password('password456'))

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

       
        product1 = Product(name='Laptop', description='A powerful laptop', price=1200.00)
        product2 = Product(name='Smartphone', description='A high-end smartphone', price=800.00)

        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()

        
        order1 = Order(
            user_id=user1.id,
            shipping_name='John Doe',
            shipping_address='123 Elm St',
            shipping_city='Springfield',
            shipping_state='IL',
            shipping_zip='62701',
            billing_name='John Doe',
            billing_address='123 Elm St',
            billing_city='Springfield',
            billing_state='IL',
            billing_zip='62701'
        )

        db.session.add(order1)
        db.session.commit()

       
        order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1)
        order_item2 = OrderItem(order_id=order1.id, product_id=product2.id, quantity=2)

        db.session.add(order_item1)
        db.session.add(order_item2)
        db.session.commit()

        
        payment1 = Payment(
            order_id=order1.id,
            card_number='1234567812345678',
            expiration='12/25',
            cvv='123'
        )

        db.session.add(payment1)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
