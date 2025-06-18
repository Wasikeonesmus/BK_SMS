from django.core.management.base import BaseCommand
from django.core import serializers
from django.conf import settings
import os
import json
from datetime import datetime
from core.models import User, Category, Product, Sale, Order, Customer, Expense, Ingredient

class Command(BaseCommand):
    help = 'Backup and restore application data to prevent data loss'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['backup', 'restore'],
            help='Action to perform: backup or restore'
        )
        parser.add_argument(
            '--filename',
            type=str,
            help='Custom filename for backup/restore'
        )

    def handle(self, *args, **options):
        action = options['action']
        filename = options.get('filename')
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'backup_{timestamp}.json'
        
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_path = os.path.join(backup_dir, filename)
        
        if action == 'backup':
            self.backup_data(backup_path)
        elif action == 'restore':
            self.restore_data(backup_path)

    def backup_data(self, backup_path):
        """Backup all important data to JSON file"""
        self.stdout.write('Starting data backup...')
        
        data = {}
        
        # Backup Users
        users = User.objects.all()
        data['users'] = serializers.serialize('json', users)
        self.stdout.write(f'Backed up {users.count()} users')
        
        # Backup Categories
        categories = Category.objects.all()
        data['categories'] = serializers.serialize('json', categories)
        self.stdout.write(f'Backed up {categories.count()} categories')
        
        # Backup Products
        products = Product.objects.all()
        data['products'] = serializers.serialize('json', products)
        self.stdout.write(f'Backed up {products.count()} products')
        
        # Backup Customers
        customers = Customer.objects.all()
        data['customers'] = serializers.serialize('json', customers)
        self.stdout.write(f'Backed up {customers.count()} customers')
        
        # Backup Sales
        sales = Sale.objects.all()
        data['sales'] = serializers.serialize('json', sales)
        self.stdout.write(f'Backed up {sales.count()} sales')
        
        # Backup Orders
        orders = Order.objects.all()
        data['orders'] = serializers.serialize('json', orders)
        self.stdout.write(f'Backed up {orders.count()} orders')
        
        # Backup Expenses
        expenses = Expense.objects.all()
        data['expenses'] = serializers.serialize('json', expenses)
        self.stdout.write(f'Backed up {expenses.count()} expenses')
        
        # Backup Ingredients
        ingredients = Ingredient.objects.all()
        data['ingredients'] = serializers.serialize('json', ingredients)
        self.stdout.write(f'Backed up {ingredients.count()} ingredients')
        
        # Save to file
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'Backup completed successfully: {backup_path}')
        )

    def restore_data(self, backup_path):
        """Restore data from JSON backup file"""
        if not os.path.exists(backup_path):
            self.stdout.write(
                self.style.ERROR(f'Backup file not found: {backup_path}')
            )
            return
        
        self.stdout.write('Starting data restore...')
        
        with open(backup_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Restore Users (skip if they already exist)
        if 'users' in data:
            users_data = json.loads(data['users'])
            for user_data in users_data:
                if not User.objects.filter(username=user_data['fields']['username']).exists():
                    user = User.objects.create_user(
                        username=user_data['fields']['username'],
                        email=user_data['fields']['email'],
                        password='admin123'  # Set default password
                    )
                    user.is_superuser = user_data['fields']['is_superuser']
                    user.is_staff = user_data['fields']['is_staff']
                    user.save()
            self.stdout.write('Users restored')
        
        # Restore Categories
        if 'categories' in data:
            categories_data = json.loads(data['categories'])
            for cat_data in categories_data:
                if not Category.objects.filter(name=cat_data['fields']['name']).exists():
                    Category.objects.create(
                        name=cat_data['fields']['name'],
                        description=cat_data['fields']['description']
                    )
            self.stdout.write('Categories restored')
        
        # Restore Products
        if 'products' in data:
            products_data = json.loads(data['products'])
            for prod_data in products_data:
                if not Product.objects.filter(sku=prod_data['fields']['sku']).exists():
                    category = None
                    if prod_data['fields']['category']:
                        category = Category.objects.filter(
                            id=prod_data['fields']['category']
                        ).first()
                    
                    Product.objects.create(
                        name=prod_data['fields']['name'],
                        description=prod_data['fields']['description'],
                        price=prod_data['fields']['price'],
                        category=category,
                        sku=prod_data['fields']['sku'],
                        current_stock=prod_data['fields']['current_stock'],
                        reorder_point=prod_data['fields']['reorder_point'],
                        cost_price=prod_data['fields']['cost_price'],
                        unit=prod_data['fields']['unit'],
                        is_active=prod_data['fields']['is_active']
                    )
            self.stdout.write('Products restored')
        
        # Restore Customers
        if 'customers' in data:
            customers_data = json.loads(data['customers'])
            for cust_data in customers_data:
                if not Customer.objects.filter(phone=cust_data['fields']['phone']).exists():
                    Customer.objects.create(
                        name=cust_data['fields']['name'],
                        phone=cust_data['fields']['phone'],
                        email=cust_data['fields']['email'],
                        address=cust_data['fields']['address']
                    )
            self.stdout.write('Customers restored')
        
        self.stdout.write(
            self.style.SUCCESS('Data restore completed successfully!')
        ) 