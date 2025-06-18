from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Category, Product, Customer
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Ensure data persistence by creating essential data if missing'

    def handle(self, *args, **options):
        self.stdout.write('Ensuring data persistence...')
        
        # Always ensure admin user exists
        self.ensure_admin_user()
        
        # Always ensure default categories exist
        self.ensure_default_categories()
        
        # Always ensure some sample products exist
        self.ensure_sample_products()
        
        # Always ensure some sample customers exist
        self.ensure_sample_customers()
        
        self.stdout.write(
            self.style.SUCCESS('Data persistence ensured successfully!')
        )

    def ensure_admin_user(self):
        """Ensure admin user always exists"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@upendobakery.com',
                password='admin123'
            )
            self.stdout.write('Created admin user')
        else:
            # Update admin password to ensure it works
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
            self.stdout.write('Updated admin user password')

    def ensure_default_categories(self):
        """Ensure default categories exist"""
        default_categories = [
            'Bread',
            'Cakes',
            'Pastries',
            'Cookies',
            'Beverages',
            'Snacks'
        ]
        
        for cat_name in default_categories:
            if not Category.objects.filter(name=cat_name).exists():
                Category.objects.create(
                    name=cat_name,
                    description=f'Various {cat_name.lower()} items'
                )
                self.stdout.write(f'Created category: {cat_name}')

    def ensure_sample_products(self):
        """Ensure some sample products exist"""
        if Product.objects.count() == 0:
            # Get first category
            category = Category.objects.first()
            if not category:
                category = Category.objects.create(name='General')
            
            sample_products = [
                {
                    'name': 'White Bread',
                    'price': Decimal('50.00'),
                    'cost_price': Decimal('30.00'),
                    'current_stock': 20,
                    'sku': 'WB001'
                },
                {
                    'name': 'Chocolate Cake',
                    'price': Decimal('800.00'),
                    'cost_price': Decimal('400.00'),
                    'current_stock': 5,
                    'sku': 'CC001'
                },
                {
                    'name': 'Croissant',
                    'price': Decimal('80.00'),
                    'cost_price': Decimal('40.00'),
                    'current_stock': 15,
                    'sku': 'CR001'
                }
            ]
            
            for product_data in sample_products:
                Product.objects.create(
                    category=category,
                    **product_data
                )
                self.stdout.write(f'Created product: {product_data["name"]}')

    def ensure_sample_customers(self):
        """Ensure some sample customers exist"""
        if Customer.objects.count() == 0:
            sample_customers = [
                {
                    'name': 'John Doe',
                    'phone': '0712345678',
                    'email': 'john@example.com'
                },
                {
                    'name': 'Jane Smith',
                    'phone': '0723456789',
                    'email': 'jane@example.com'
                }
            ]
            
            for customer_data in sample_customers:
                Customer.objects.create(**customer_data)
                self.stdout.write(f'Created customer: {customer_data["name"]}') 