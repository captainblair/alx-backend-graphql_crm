#!/usr/bin/env python
"""
Seed script to populate the CRM database with sample data.
Run with: python seed_db.py
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from crm.models import Customer, Product, Order
from decimal import Decimal


def clear_data():
    """Clear all existing data"""
    print("Clearing existing data...")
    Order.objects.all().delete()
    Customer.objects.all().delete()
    Product.objects.all().delete()
    print("✓ Data cleared")


def create_customers():
    """Create sample customers"""
    print("\nCreating customers...")
    customers_data = [
        {"name": "Alice Johnson", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob Smith", "email": "bob@example.com", "phone": "123-456-7890"},
        {"name": "Carol Williams", "email": "carol@example.com", "phone": "+9876543210"},
        {"name": "David Brown", "email": "david@example.com", "phone": "987-654-3210"},
        {"name": "Eve Davis", "email": "eve@example.com", "phone": "+1122334455"},
    ]
    
    customers = []
    for data in customers_data:
        customer = Customer.objects.create(**data)
        customers.append(customer)
        print(f"  ✓ Created customer: {customer.name}")
    
    return customers


def create_products():
    """Create sample products"""
    print("\nCreating products...")
    products_data = [
        {"name": "Laptop", "price": Decimal("999.99"), "stock": 10},
        {"name": "Mouse", "price": Decimal("29.99"), "stock": 50},
        {"name": "Keyboard", "price": Decimal("79.99"), "stock": 30},
        {"name": "Monitor", "price": Decimal("299.99"), "stock": 15},
        {"name": "Headphones", "price": Decimal("149.99"), "stock": 25},
        {"name": "Webcam", "price": Decimal("89.99"), "stock": 20},
        {"name": "USB Cable", "price": Decimal("9.99"), "stock": 100},
    ]
    
    products = []
    for data in products_data:
        product = Product.objects.create(**data)
        products.append(product)
        print(f"  ✓ Created product: {product.name} - ${product.price}")
    
    return products


def create_orders(customers, products):
    """Create sample orders"""
    print("\nCreating orders...")
    
    # Order 1: Alice buys Laptop and Mouse
    order1 = Order.objects.create(
        customer=customers[0],
        total_amount=products[0].price + products[1].price
    )
    order1.products.set([products[0], products[1]])
    print(f"  ✓ Created order for {customers[0].name}: ${order1.total_amount}")
    
    # Order 2: Bob buys Keyboard, Monitor, and Headphones
    order2 = Order.objects.create(
        customer=customers[1],
        total_amount=products[2].price + products[3].price + products[4].price
    )
    order2.products.set([products[2], products[3], products[4]])
    print(f"  ✓ Created order for {customers[1].name}: ${order2.total_amount}")
    
    # Order 3: Carol buys Webcam and USB Cable
    order3 = Order.objects.create(
        customer=customers[2],
        total_amount=products[5].price + products[6].price
    )
    order3.products.set([products[5], products[6]])
    print(f"  ✓ Created order for {customers[2].name}: ${order3.total_amount}")
    
    # Order 4: David buys Mouse and USB Cable
    order4 = Order.objects.create(
        customer=customers[3],
        total_amount=products[1].price + products[6].price
    )
    order4.products.set([products[1], products[6]])
    print(f"  ✓ Created order for {customers[3].name}: ${order4.total_amount}")
    
    # Order 5: Eve buys Laptop, Monitor, and Headphones
    order5 = Order.objects.create(
        customer=customers[4],
        total_amount=products[0].price + products[3].price + products[4].price
    )
    order5.products.set([products[0], products[3], products[4]])
    print(f"  ✓ Created order for {customers[4].name}: ${order5.total_amount}")


def print_summary():
    """Print database summary"""
    print("\n" + "="*50)
    print("DATABASE SUMMARY")
    print("="*50)
    print(f"Total Customers: {Customer.objects.count()}")
    print(f"Total Products: {Product.objects.count()}")
    print(f"Total Orders: {Order.objects.count()}")
    print("="*50)


def main():
    print("="*50)
    print("CRM DATABASE SEEDING SCRIPT")
    print("="*50)
    
    # Clear existing data
    clear_data()
    
    # Create data
    customers = create_customers()
    products = create_products()
    create_orders(customers, products)
    
    # Print summary
    print_summary()
    
    print("\n✓ Database seeding completed successfully!")


if __name__ == '__main__':
    main()
