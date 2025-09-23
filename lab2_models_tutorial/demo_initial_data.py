#!/usr/bin/env python
"""
Django Initial Data Tutorial - Demo Script

This script demonstrates both approaches for providing initial data:
1. Data Migrations
2. Fixtures

Run this script to see practical examples of loading initial data.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section"""
    print(f"\n--- {title} ---")

def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n🔹 {description}")
    print(f"Command: {command}")
    print("-" * 40)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists and print result"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} not found: {filepath}")
        return False

def main():
    print_header("Django Initial Data Tutorial - Demo")
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: This script must be run from the Django project directory")
        print("   (directory containing manage.py)")
        sys.exit(1)
    
    print("✅ Found Django project (manage.py exists)")
    
    # Section 1: Check fixture files
    print_section("1. Checking Fixture Files")
    
    fixture_files = [
        ("library/fixtures/initial_authors.json", "Authors fixture"),
        ("library/fixtures/initial_categories.json", "Categories fixture"),
        ("library/fixtures/initial_books.json", "Books fixture"),
        ("library/fixtures/initial_reviews.json", "Reviews fixture"),
        ("library/fixtures/library_sample_data.json", "Sample data fixture"),
        ("library/fixtures/additional_books.yaml", "YAML fixture"),
    ]
    
    all_fixtures_exist = True
    for filepath, description in fixture_files:
        if not check_file_exists(filepath, description):
            all_fixtures_exist = False
    
    if all_fixtures_exist:
        print("\n✅ All fixture files are present!")
    else:
        print("\n⚠️  Some fixture files are missing. Please run the tutorial setup first.")
    
    # Section 2: Check data migration
    print_section("2. Checking Data Migration")
    
    migration_file = "library/migrations/0003_load_initial_data.py"
    if check_file_exists(migration_file, "Data migration"):
        print("✅ Data migration is ready!")
    else:
        print("❌ Data migration not found. Please run: python manage.py makemigrations library --empty --name=load_initial_data")
    
    # Section 3: Database operations
    print_section("3. Database Operations")
    
    # Check current database state
    run_command("python manage.py showmigrations library", 
                "Checking migration status")
    
    # Section 4: Demonstrate fixture loading
    print_section("4. Fixture Loading Demonstration")
    
    print("\n🔹 Available fixture loading commands:")
    commands = [
        "python manage.py loaddata initial_authors",
        "python manage.py loaddata initial_categories", 
        "python manage.py loaddata initial_books",
        "python manage.py loaddata initial_reviews",
        "python manage.py loaddata library_sample_data",
        "python manage.py loaddata additional_books.yaml",
        "python manage.py loaddata initial_authors initial_categories initial_books",
    ]
    
    for cmd in commands:
        print(f"  📋 {cmd}")
    
    # Section 5: Demonstrate data migration
    print_section("5. Data Migration Demonstration")
    
    print("\n🔹 Data migration commands:")
    migration_commands = [
        "python manage.py migrate library",  # Apply all migrations including data migration
        "python manage.py migrate library 0002",  # Rollback to before data migration
        "python manage.py migrate library 0003",  # Apply data migration specifically
    ]
    
    for cmd in migration_commands:
        print(f"  📋 {cmd}")
    
    # Section 6: Utility commands
    print_section("6. Utility Commands")
    
    print("\n🔹 Useful commands for working with initial data:")
    utility_commands = [
        "python manage.py dumpdata library --indent 2 > backup.json  # Create backup",
        "python manage.py loaddata --verbosity=2 initial_authors     # Verbose loading",
        "python manage.py flush                                       # Clear all data",
        "python manage.py shell                                       # Django shell",
        "python manage.py dbshell                                     # Database shell",
    ]
    
    for cmd in utility_commands:
        print(f"  📋 {cmd}")
    
    # Section 7: Interactive demonstration
    print_section("7. Interactive Demonstration")
    
    response = input("\n🤔 Would you like to run an interactive demonstration? (y/n): ").lower()
    
    if response == 'y':
        print("\n🚀 Starting interactive demonstration...")
        
        # Clear existing data
        print("\n1. Clearing existing data...")
        if run_command("python manage.py flush --noinput", "Clearing database"):
            print("✅ Database cleared")
        
        # Apply migrations (including data migration)
        print("\n2. Applying migrations (including data migration)...")
        if run_command("python manage.py migrate", "Applying migrations"):
            print("✅ Migrations applied (data migration included)")
        
        # Check what data was created by migration
        print("\n3. Checking data created by migration...")
        run_command("python manage.py shell -c \"from library.models import *; print(f'Authors: {Author.objects.count()}'); print(f'Categories: {Category.objects.count()}'); print(f'Books: {Book.objects.count()}')\"",
                   "Counting objects from data migration")
        
        # Load fixture data
        print("\n4. Loading additional data from fixtures...")
        if run_command("python manage.py loaddata library_sample_data", "Loading sample data fixture"):
            print("✅ Sample data loaded")
        
        # Final count
        print("\n5. Final data count...")
        run_command("python manage.py shell -c \"from library.models import *; print(f'Total Authors: {Author.objects.count()}'); print(f'Total Categories: {Category.objects.count()}'); print(f'Total Books: {Book.objects.count()}')\"",
                   "Final object counts")
        
        print("\n✅ Interactive demonstration complete!")
        print("💡 You can now explore the data using the Django admin or shell")
        
    else:
        print("\n📚 Demo completed. Use the commands above to explore initial data loading.")
    
    # Section 8: Summary
    print_section("8. Summary")
    
    print("""
✅ This tutorial demonstrated:
   • Creating JSON and YAML fixtures
   • Writing data migrations with forward/reverse operations
   • Loading fixtures with the loaddata command
   • Using get_or_create() to avoid duplicates
   • Best practices for initial data management

📖 Key files created:
   • library/fixtures/*.json - JSON fixture files
   • library/fixtures/additional_books.yaml - YAML fixture example
   • library/migrations/0003_load_initial_data.py - Data migration
   • DJANGO_INITIAL_DATA_TUTORIAL.md - Complete documentation

🎯 Next steps:
   • Try modifying the fixtures and reloading
   • Create your own data migration
   • Practice with dumpdata and loaddata commands
   • Integrate initial data into your deployment process

📚 For more information, see:
   • DJANGO_INITIAL_DATA_TUTORIAL.md
   • https://docs.djangoproject.com/en/4.1/howto/initial-data/
    """)

if __name__ == "__main__":
    main()
