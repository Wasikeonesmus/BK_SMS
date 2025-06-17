from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Create default categories for the bakery'

    def handle(self, *args, **options):
        default_categories = [
            {
                'name': 'Bread',
                'description': 'Various types of bread including white, brown, whole wheat, and specialty breads'
            },
            {
                'name': 'Cakes',
                'description': 'Birthday cakes, wedding cakes, and other celebration cakes'
            },
            {
                'name': 'Pastries',
                'description': 'Croissants, danishes, muffins, and other pastries'
            },
            {
                'name': 'Cookies',
                'description': 'Chocolate chip, oatmeal, sugar cookies and other varieties'
            },
            {
                'name': 'Pies',
                'description': 'Apple pie, meat pie, and other pie varieties'
            },
            {
                'name': 'Buns',
                'description': 'Sweet buns, hot cross buns, and other bun varieties'
            },
            {
                'name': 'Snacks',
                'description': 'Quick snacks and finger foods'
            },
            {
                'name': 'Beverages',
                'description': 'Coffee, tea, juices, and other drinks'
            },
            {
                'name': 'Ingredients',
                'description': 'Raw ingredients for baking'
            },
            {
                'name': 'Other',
                'description': 'Miscellaneous bakery items'
            }
        ]

        created_count = 0
        for category_data in default_categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories')
        ) 