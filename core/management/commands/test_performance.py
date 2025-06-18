from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Product, Category, Sale, Order, Customer
from decimal import Decimal
import time
import statistics

User = get_user_model()

class Command(BaseCommand):
    help = 'Test application performance by simulating common user actions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--iterations',
            type=int,
            default=10,
            help='Number of iterations to run for each test'
        )

    def handle(self, *args, **options):
        iterations = options['iterations']
        
        # Create test data if needed
        self.create_test_data()
        
        # Create test client
        client = Client()
        
        # Create test user and login
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
        
        client.login(username='admin', password='admin123')
        
        # Test performance
        self.stdout.write(self.style.SUCCESS('Starting performance tests...'))
        
        # Test dashboard
        self.test_dashboard_performance(client, iterations)
        
        # Test POS
        self.test_pos_performance(client, iterations)
        
        # Test inventory
        self.test_inventory_performance(client, iterations)
        
        # Test sales
        self.test_sales_performance(client, iterations)
        
        # Test reports
        self.test_reports_performance(client, iterations)
        
        self.stdout.write(self.style.SUCCESS('Performance tests completed!'))

    def create_test_data(self):
        """Create test data if it doesn't exist"""
        if Category.objects.count() == 0:
            category = Category.objects.create(name='Test Category')
            self.stdout.write('Created test category')
        else:
            category = Category.objects.first()
        
        if Product.objects.count() == 0:
            for i in range(50):
                Product.objects.create(
                    name=f'Test Product {i}',
                    price=Decimal('100.00'),
                    category=category,
                    current_stock=100,
                    reorder_point=10
                )
            self.stdout.write('Created 50 test products')
        
        if Customer.objects.count() == 0:
            for i in range(20):
                Customer.objects.create(
                    name=f'Test Customer {i}',
                    phone=f'07{i:08d}',
                    email=f'customer{i}@test.com'
                )
            self.stdout.write('Created 20 test customers')

    def measure_performance(self, func, iterations):
        """Measure performance of a function"""
        times = []
        for i in range(iterations):
            start_time = time.time()
            func()
            end_time = time.time()
            times.append(end_time - start_time)
        
        return {
            'min': min(times),
            'max': max(times),
            'avg': statistics.mean(times),
            'median': statistics.median(times),
            'std': statistics.stdev(times) if len(times) > 1 else 0
        }

    def test_dashboard_performance(self, client, iterations):
        self.stdout.write('\nTesting Dashboard Performance...')
        
        def test_dashboard():
            response = client.get(reverse('dashboard'))
            return response.status_code == 200
        
        results = self.measure_performance(test_dashboard, iterations)
        self.print_results('Dashboard', results)

    def test_pos_performance(self, client, iterations):
        self.stdout.write('\nTesting POS Performance...')
        
        def test_pos():
            response = client.get(reverse('pos'))
            return response.status_code == 200
        
        results = self.measure_performance(test_pos, iterations)
        self.print_results('POS', results)

    def test_inventory_performance(self, client, iterations):
        self.stdout.write('\nTesting Inventory Performance...')
        
        def test_inventory():
            response = client.get(reverse('inventory'))
            return response.status_code == 200
        
        results = self.measure_performance(test_inventory, iterations)
        self.print_results('Inventory', results)

    def test_sales_performance(self, client, iterations):
        self.stdout.write('\nTesting Sales Performance...')
        
        def test_sales():
            response = client.get(reverse('sales'))
            return response.status_code == 200
        
        results = self.measure_performance(test_sales, iterations)
        self.print_results('Sales', results)

    def test_reports_performance(self, client, iterations):
        self.stdout.write('\nTesting Reports Performance...')
        
        def test_reports():
            response = client.get(reverse('reports'))
            return response.status_code == 200
        
        results = self.measure_performance(test_reports, iterations)
        self.print_results('Reports', results)

    def print_results(self, test_name, results):
        self.stdout.write(f'{test_name}:')
        self.stdout.write(f'  Average: {results["avg"]:.3f}s')
        self.stdout.write(f'  Median:  {results["median"]:.3f}s')
        self.stdout.write(f'  Min:     {results["min"]:.3f}s')
        self.stdout.write(f'  Max:     {results["max"]:.3f}s')
        self.stdout.write(f'  Std Dev: {results["std"]:.3f}s')
        
        # Color code based on performance
        if results["avg"] < 0.5:
            self.stdout.write(self.style.SUCCESS('  Status: Excellent'))
        elif results["avg"] < 1.0:
            self.stdout.write(self.style.WARNING('  Status: Good'))
        else:
            self.stdout.write(self.style.ERROR('  Status: Needs Improvement')) 