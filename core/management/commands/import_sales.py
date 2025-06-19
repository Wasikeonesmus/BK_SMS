import csv
from django.core.management.base import BaseCommand
from core.models import Product, Sale
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

class Command(BaseCommand):
    help = 'Import sales from a CSV file. Columns: product_sku,quantity,payment_type'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('--user', type=str, help='Username to assign as cashier for the sales', default=None)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        username = options['user']
        User = get_user_model()
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User {username} does not exist.'))
                return
        else:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                self.stdout.write(self.style.ERROR('No user found to assign to sales. Use --user to specify.'))
                return

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            errors = 0
            for row in reader:
                sku = row.get('product_sku')
                qty = int(row.get('quantity', 0))
                payment_type = row.get('payment_type', 'cash')
                try:
                    product = Product.objects.get(sku=sku)
                    if product.current_stock < qty:
                        self.stdout.write(self.style.WARNING(f'Not enough stock for {sku} ({product.name}). Skipping.'))
                        errors += 1
                        continue
                    with transaction.atomic():
                        Sale.objects.create(
                            product=product,
                            qty=qty,
                            price=product.price,
                            payment_type=payment_type,
                            user=user,
                            date=timezone.now()
                        )
                        product.current_stock -= qty
                        product.save()
                        count += 1
                except Product.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Product with SKU {sku} does not exist. Skipping.'))
                    errors += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing row {row}: {e}'))
                    errors += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {count} sales. {errors} errors.')) 