# Generated manually for performance optimization

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_order_payment_type'),
    ]

    operations = [
        # Add indexes for frequently queried fields
        migrations.RunSQL(
            # Add indexes
            """
            CREATE INDEX IF NOT EXISTS idx_sale_date ON core_sale(date);
            CREATE INDEX IF NOT EXISTS idx_sale_product ON core_sale(product_id);
            CREATE INDEX IF NOT EXISTS idx_sale_payment_type ON core_sale(payment_type);
            CREATE INDEX IF NOT EXISTS idx_order_status ON core_order(status);
            CREATE INDEX IF NOT EXISTS idx_order_created_at ON core_order(created_at);
            CREATE INDEX IF NOT EXISTS idx_order_customer ON core_order(customer_id);
            CREATE INDEX IF NOT EXISTS idx_product_category ON core_product(category_id);
            CREATE INDEX IF NOT EXISTS idx_product_active ON core_product(is_active);
            CREATE INDEX IF NOT EXISTS idx_product_stock ON core_product(current_stock);
            CREATE INDEX IF NOT EXISTS idx_expense_date ON core_expense(date);
            CREATE INDEX IF NOT EXISTS idx_customer_phone ON core_customer(phone);
            CREATE INDEX IF NOT EXISTS idx_customer_created_at ON core_customer(created_at);
            CREATE INDEX IF NOT EXISTS idx_ingredient_name ON core_ingredient(name);
            CREATE INDEX IF NOT EXISTS idx_employee_user ON core_employee(user_id);
            CREATE INDEX IF NOT EXISTS idx_supplier_name ON core_supplier(name);
            CREATE INDEX IF NOT EXISTS idx_purchaseorder_supplier ON core_purchaseorder(supplier_id);
            CREATE INDEX IF NOT EXISTS idx_purchaseorder_status ON core_purchaseorder(status);
            CREATE INDEX IF NOT EXISTS idx_stockhistory_product ON core_stockhistory(product_id);
            CREATE INDEX IF NOT EXISTS idx_stockhistory_date ON core_stockhistory(date);
            """,
            # Remove indexes (reverse migration)
            """
            DROP INDEX IF EXISTS idx_sale_date;
            DROP INDEX IF EXISTS idx_sale_product;
            DROP INDEX IF EXISTS idx_sale_payment_type;
            DROP INDEX IF EXISTS idx_order_status;
            DROP INDEX IF EXISTS idx_order_created_at;
            DROP INDEX IF EXISTS idx_order_customer;
            DROP INDEX IF EXISTS idx_product_category;
            DROP INDEX IF EXISTS idx_product_active;
            DROP INDEX IF EXISTS idx_product_stock;
            DROP INDEX IF EXISTS idx_expense_date;
            DROP INDEX IF EXISTS idx_customer_phone;
            DROP INDEX IF EXISTS idx_customer_created_at;
            DROP INDEX IF EXISTS idx_ingredient_name;
            DROP INDEX IF EXISTS idx_employee_user;
            DROP INDEX IF EXISTS idx_supplier_name;
            DROP INDEX IF EXISTS idx_purchaseorder_supplier;
            DROP INDEX IF EXISTS idx_purchaseorder_status;
            DROP INDEX IF EXISTS idx_stockhistory_product;
            DROP INDEX IF EXISTS idx_stockhistory_date;
            """
        ),
    ] 