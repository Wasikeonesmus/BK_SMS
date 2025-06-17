from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Category

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a default admin user for the bakery'

    def handle(self, *args, **options):
        # Create default admin user
        username = 'admin'
        email = 'admin@upendobakery.com'
        password = 'admin123'
        
        try:
            # Check if admin user already exists
            if User.objects.filter(username=username).exists():
                admin_user = User.objects.get(username=username)
                # Update password to ensure it's correct
                admin_user.set_password(password)
                admin_user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated existing admin user: {username}')
                )
            else:
                # Create new admin user
                admin_user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    role='admin'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created new admin user: {username}')
                )
            
            # Also create a test user for regular access
            test_username = 'testuser'
            test_password = 'test123'
            
            if User.objects.filter(username=test_username).exists():
                test_user = User.objects.get(username=test_username)
                test_user.set_password(test_password)
                test_user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated existing test user: {test_username}')
                )
            else:
                test_user = User.objects.create_user(
                    username=test_username,
                    email='test@upendobakery.com',
                    password=test_password,
                    role='cashier'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created new test user: {test_username}')
                )
            
            self.stdout.write(
                self.style.SUCCESS('Default users created successfully!')
            )
            self.stdout.write(
                self.style.WARNING('Admin credentials:')
            )
            self.stdout.write(
                self.style.WARNING(f'Username: {username}')
            )
            self.stdout.write(
                self.style.WARNING(f'Password: {password}')
            )
            self.stdout.write(
                self.style.WARNING('Test user credentials:')
            )
            self.stdout.write(
                self.style.WARNING(f'Username: {test_username}')
            )
            self.stdout.write(
                self.style.WARNING(f'Password: {test_password}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating default users: {str(e)}')
            ) 