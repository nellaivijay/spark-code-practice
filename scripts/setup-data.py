#!/usr/bin/env python3
"""
Spark Code Practice - Data Setup Script
This script downloads and sets up sample data for the labs.
"""

import os
import sys
import urllib.request
import zipfile
import json
from pathlib import Path

def download_file(url, destination):
    """Download a file from URL to destination."""
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"✅ Downloaded to {destination}")
        return True
    except Exception as e:
        print(f"❌ Failed to download: {e}")
        return False

def create_sample_data():
    """Create sample data files for labs."""
    data_dir = Path("data/sample")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample CSV data
    csv_data = """name,age,department,salary
Alice,28,Engineering,75000
Bob,32,Marketing,65000
Charlie,35,Engineering,85000
Diana,29,Sales,60000
Eve,31,Marketing,70000
Frank,27,Engineering,72000
Grace,33,Sales,68000
Henry,36,Engineering,90000
Ivy,26,Marketing,62000
Jack,34,Sales,71000"""
    
    csv_file = data_dir / "employees.csv"
    with open(csv_file, 'w') as f:
        f.write(csv_data)
    print(f"✅ Created sample CSV: {csv_file}")
    
    # Create sample JSON data
    json_data = [
        {"id": 1, "name": "Alice", "age": 28, "skills": ["Python", "Spark", "SQL"]},
        {"id": 2, "name": "Bob", "age": 32, "skills": ["Java", "Hadoop"]},
        {"id": 3, "name": "Charlie", "age": 35, "skills": ["Python", "ML", "TensorFlow"]},
        {"id": 4, "name": "Diana", "age": 29, "skills": ["R", "Statistics"]},
        {"id": 5, "name": "Eve", "age": 31, "skills": ["Python", "AWS", "Docker"]}
    ]
    
    json_file = data_dir / "employees.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"✅ Created sample JSON: {json_file}")
    
    # Create sample sales data for aggregations
    sales_csv = """date,product,category,quantity,revenue
2024-01-01,Laptop,Electronics,2,2000
2024-01-01,Mouse,Electronics,5,50
2024-01-02,Desk,Furniture,1,300
2024-01-02,Chair,Furniture,4,400
2024-01-03,Monitor,Electronics,3,900
2024-01-03,Keyboard,Electronics,5,150
2024-01-04,Bookcase,Furniture,2,200
2024-01-04,Table,Furniture,1,500
2024-01-05,Headphones,Electronics,4,400
2024-01-05,Lamp,Furniture,3,90"""
    
    sales_file = data_dir / "sales.csv"
    with open(sales_file, 'w') as f:
        f.write(sales_csv)
    print(f"✅ Created sample sales CSV: {sales_file}")
    
    print(f"\n✅ Sample data created in {data_dir}")

def setup_directories():
    """Create necessary directories for the labs."""
    directories = [
        "data/sample",
        "data/parquet",
        "data/json",
        "data/csv",
        "logs",
        "checkpoint",
        "notebooks",
        "solutions"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function."""
    print("🚀 Setting up Spark Code Practice data...")
    print()
    
    # Create directories
    print("📁 Creating directories...")
    setup_directories()
    print()
    
    # Create sample data
    print("📊 Creating sample data...")
    create_sample_data()
    print()
    
    print("✅ Data setup complete!")
    print()
    print("📝 Next steps:")
    print("  1. Run: ./scripts/setup.sh")
    print("  2. Run: ./scripts/start.sh")
    print("  3. Access Jupyter at http://localhost:8888")
    print("  4. Start with Lab 1: Spark Fundamentals")

if __name__ == "__main__":
    main()
