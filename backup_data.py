#!/usr/bin/env python
"""
Simple data backup script for Upendo Bakery
Run this before restarting the server to backup your data
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'upendo_bakery.settings')

# Initialize Django
django.setup()

from core.models import User, Category, Product, Sale, Order, Customer, Expense

def backup_data():
    """Backup all important data to JSON file"""
    print("Starting data backup...")
    
    # Create backups directory
    backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
    
    data = {}
    
    # Backup Users (without passwords)
    users = User.objects.all()
    user_data = []
    for user in users:
        user_data.append({
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined.isoformat() if user.date_joined else None
        })
    data['users'] = user_data
    print(f"Backed up {len(user_data)} users")
    
    # Backup Categories
    categories = Category.objects.all()
    category_data = []
    for cat in categories:
        category_data.append({
            'name': cat.name,
            'description': cat.description
        })
    data['categories'] = category_data
    print(f"Backed up {len(category_data)} categories")
    
    # Backup Products
    products = Product.objects.all()
    product_data = []
    for prod in products:
        product_data.append({
            'name': prod.name,
            'description': prod.description,
            'price': str(prod.price),
            'cost_price': str(prod.cost_price),
            'current_stock': prod.current_stock,
            'reorder_point': prod.reorder_point,
            'sku': prod.sku,
            'unit': prod.unit,
            'is_active': prod.is_active,
            'category_name': prod.category.name if prod.category else None
        })
    data['products'] = product_data
    print(f"Backed up {len(product_data)} products")
    
    # Backup Customers
    customers = Customer.objects.all()
    customer_data = []
    for cust in customers:
        customer_data.append({
            'name': cust.name,
            'phone': cust.phone,
            'email': cust.email,
            'address': cust.address
        })
    data['customers'] = customer_data
    print(f"Backed up {len(customer_data)} customers")
    
    # Backup Sales
    sales = Sale.objects.all()
    sale_data = []
    for sale in sales:
        sale_data.append({
            'product_name': sale.product.name if sale.product else None,
            'quantity': sale.quantity,
            'total_amount': str(sale.total_amount),
            'date': sale.date.isoformat() if sale.date else None
        })
    data['sales'] = sale_data
    print(f"Backed up {len(sale_data)} sales")
    
    # Backup Orders
    orders = Order.objects.all()
    order_data = []
    for order in orders:
        order_data.append({
            'customer_name': order.customer.name if order.customer else None,
            'total_amount': str(order.total_amount),
            'payment_type': order.payment_type,
            'status': order.status,
            'created_at': order.created_at.isoformat() if order.created_at else None
        })
    data['orders'] = order_data
    print(f"Backed up {len(order_data)} orders")
    
    # Save to file
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Backup completed successfully: {backup_file}")
    return backup_file

def restore_data(backup_file):
    """Restore data from backup file"""
    if not os.path.exists(backup_file):
        print(f"Backup file not found: {backup_file}")
        return
    
    print(f"Restoring data from: {backup_file}")
    
    with open(backup_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Restore Categories
    if 'categories' in data:
        for cat_data in data['categories']:
            if not Category.objects.filter(name=cat_data['name']).exists():
                Category.objects.create(**cat_data)
        print("Categories restored")
    
    # Restore Products
    if 'products' in data:
        for prod_data in data['products']:
            if not Product.objects.filter(sku=prod_data['sku']).exists():
                # Get category
                category = None
                if prod_data['category_name']:
                    category = Category.objects.filter(name=prod_data['category_name']).first()
                
                # Convert price strings back to Decimal
                from decimal import Decimal
                prod_data['price'] = Decimal(prod_data['price'])
                prod_data['cost_price'] = Decimal(prod_data['cost_price'])
                
                # Remove category_name and add category
                category_name = prod_data.pop('category_name')
                prod_data['category'] = category
                
                Product.objects.create(**prod_data)
        print("Products restored")
    
    # Restore Customers
    if 'customers' in data:
        for cust_data in data['customers']:
            if not Customer.objects.filter(phone=cust_data['phone']).exists():
                Customer.objects.create(**cust_data)
        print("Customers restored")
    
    print("Data restoration completed!")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Backup or restore Upendo Bakery data')
    parser.add_argument('action', choices=['backup', 'restore'], help='Action to perform')
    parser.add_argument('--file', help='Backup file for restore operation')
    
    args = parser.parse_args()
    
    if args.action == 'backup':
        backup_data()
    elif args.action == 'restore':
        if not args.file:
            print("Please specify backup file with --file")
            sys.exit(1)
        restore_data(args.file)