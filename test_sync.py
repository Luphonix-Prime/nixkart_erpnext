#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.management.commands.sync_erpnext import Command
from store.models import Product, Category

def test_sync():
    print("Testing ERPNext synchronization...")
    
    # Run the sync command
    command = Command()
    command.handle()
    
    # Check if products were synced
    products = Product.objects.all()
    categories = Category.objects.all()
    
    print(f"Total products synced: {products.count()}")
    print(f"Total categories synced: {categories.count()}")
    
    # Display some product information
    for product in products[:5]:
        print(f"Product: {product.name}, Price: {product.price}, Stock: {product.stock}")
        
    # Display some category information
    for category in categories[:5]:
        print(f"Category: {category.name}")
    
    # Test if we can fetch products through the data adapter
    print("\nTesting data adapter...")
    from store.data_adapter import DataAdapter
    try:
        test_products = DataAdapter.get_products(limit=5)
        print(f"Successfully fetched {len(test_products)} products through data adapter")
        for product in test_products:
            if isinstance(product, dict):
                print(f"  - {product.get('name', 'Unknown')} (Price: {product.get('price', 0)})")
            else:
                print(f"  - {product.name} (Price: {product.price})")
    except Exception as e:
        print(f"Error fetching products through data adapter: {e}")

if __name__ == "__main__":
    test_sync()