#!/usr/bin/env python
"""
Interactive Django Migrations Tutorial

Run this script to see live migration examples:
python manage.py shell
>>> exec(open('migrations_interactive_demo.py').read())
"""

import os
import sys
import django
from datetime import date, datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from django.apps import apps
from io import StringIO
import contextlib

def capture_command_output(command, *args, **kwargs):
    """Capture output from Django management commands"""
    output = StringIO()
    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            call_command(command, *args, **kwargs, verbosity=2)
        return output.getvalue()
    except Exception as e:
        return f"Error: {str(e)}"

def show_migration_status():
    """Show current migration status"""
    print("📊 Current Migration Status:")
    print("-" * 40)
    
    output = capture_command_output('showmigrations')
    print(output)

def demo_initial_migration():
    """Demonstrate creating initial migration for library app"""
    print("\n" + "=" * 60)
    print("DEMO: Creating Initial Migration")
    print("=" * 60)
    
    print("\n1. We've created a new 'library' app with models:")
    print("   • Author (name, email, birth_date, bio)")
    print("   • Category (name, description)")
    print("   • Book (title, author, category, publication_date, etc.)")
    print("   • Review (book, reviewer_name, rating, comment)")
    
    print("\n2. Creating initial migration:")
    print("Command: python manage.py makemigrations library")
    
    try:
        output = capture_command_output('makemigrations', 'library', verbosity=2)
        print("Output:")
        print(output)
    except Exception as e:
        print(f"Note: {e}")
    
    print("\n3. Let's see what the migration file contains:")
    try:
        # Try to import the library models
        import library.models
        print("Migration file created successfully!")
    except:
        print("Migration file will be created when you run the command above.")

def demo_applying_migrations():
    """Demonstrate applying migrations"""
    print("\n" + "=" * 60)
    print("DEMO: Applying Migrations")
    print("=" * 60)
    
    print("\n1. Applying migrations to database:")
    print("Command: python manage.py migrate")
    
    try:
        output = capture_command_output('migrate', verbosity=2)
        print("Output:")
        print(output)
    except Exception as e:
        print(f"Output: {e}")
    
    print("\n2. Checking migration status after applying:")
    show_migration_status()

def demo_sql_migration():
    """Show SQL for migrations"""
    print("\n" + "=" * 60)
    print("DEMO: Viewing Migration SQL")
    print("=" * 60)
    
    print("\n1. Viewing SQL for blog app's initial migration:")
    print("Command: python manage.py sqlmigrate blog 0001")
    
    try:
        output = capture_command_output('sqlmigrate', 'blog', '0001')
        print("SQL Output:")
        print("-" * 40)
        print(output)
    except Exception as e:
        print(f"Note: {e}")

def demo_model_changes():
    """Demonstrate model changes and migrations"""
    print("\n" + "=" * 60)
    print("DEMO: Model Changes and New Migrations")
    print("=" * 60)
    
    print("\n📝 Let's simulate adding a new field to the Author model:")
    
    new_field_code = '''
# Add this field to Author model:
website = models.URLField(blank=True, null=True)
'''
    
    print("Model change:")
    print(new_field_code)
    
    print("\n💡 After adding this field, you would:")
    print("1. Run: python manage.py makemigrations")
    print("2. Review the generated migration file")
    print("3. Run: python manage.py migrate")
    
    print("\n📋 The migration would contain:")
    migration_code = '''
operations = [
    migrations.AddField(
        model_name='author',
        name='website',
        field=models.URLField(blank=True, null=True),
    ),
]
'''
    print(migration_code)

def demo_data_migration_example():
    """Show example of data migration"""
    print("\n" + "=" * 60)
    print("DEMO: Data Migration Example")
    print("=" * 60)
    
    print("\n📊 Data migrations are used to modify existing data.")
    print("Example: Updating all books to have a default category")
    
    data_migration_code = '''
# Example data migration file: 0003_set_default_category.py
from django.db import migrations

def set_default_category(apps, schema_editor):
    """Set default category for books without one"""
    Book = apps.get_model("library", "Book")
    Category = apps.get_model("library", "Category")
    
    # Create default category if it doesn't exist
    default_category, created = Category.objects.get_or_create(
        name="General",
        defaults={"description": "General category for uncategorized books"}
    )
    
    # Update books without category
    books_without_category = Book.objects.filter(category__isnull=True)
    books_without_category.update(category=default_category)
    
    print(f"Updated {books_without_category.count()} books with default category")

def reverse_default_category(apps, schema_editor):
    """Reverse the default category assignment"""
    Book = apps.get_model("library", "Book")
    Category = apps.get_model("library", "Category")
    
    try:
        default_category = Category.objects.get(name="General")
        Book.objects.filter(category=default_category).update(category=None)
        # Optionally delete the default category if no other books use it
        if not Book.objects.filter(category=default_category).exists():
            default_category.delete()
    except Category.DoesNotExist:
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('library', '0002_book_add_category'),
    ]

    operations = [
        migrations.RunPython(
            set_default_category,
            reverse_default_category
        ),
    ]
'''
    
    print("Data migration example:")
    print(data_migration_code)
    
    print("\n💡 To create an empty migration for data migration:")
    print("Command: python manage.py makemigrations --empty library")

def demo_migration_dependencies():
    """Show migration dependencies"""
    print("\n" + "=" * 60)
    print("DEMO: Migration Dependencies")
    print("=" * 60)
    
    print("\n🔗 Dependencies ensure migrations run in the correct order:")
    
    dependency_example = '''
class Migration(migrations.Migration):
    dependencies = [
        ('library', '0001_initial'),        # Previous migration in same app
        ('auth', '0012_alter_user_first_name'),  # Django's auth app migration
        ('blog', '0001_initial'),           # Another app's migration
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('user', models.OneToOneField('auth.User', on_delete=models.CASCADE)),
                ('favorite_books', models.ManyToManyField('library.Book')),
                ('library_card', models.CharField(max_length=20)),
            ],
        ),
    ]
'''
    
    print("Example migration with dependencies:")
    print(dependency_example)
    
    print("\n📋 Why dependencies matter:")
    print("• Ensure referenced tables exist before creating foreign keys")
    print("• Maintain data integrity across app boundaries")
    print("• Allow Django to determine correct migration order")

def demo_reversing_migrations():
    """Demonstrate migration reversal"""
    print("\n" + "=" * 60)
    print("DEMO: Reversing Migrations")
    print("=" * 60)
    
    print("\n⏪ Migrations can be reversed to undo changes:")
    
    print("\n📋 Reversal commands:")
    reversal_commands = [
        ("Reverse to specific migration", "python manage.py migrate library 0001"),
        ("Reverse all migrations", "python manage.py migrate library zero"),
        ("Show migration plan", "python manage.py migrate --plan library 0001"),
        ("Fake reverse (mark as unapplied)", "python manage.py migrate --fake library 0001")
    ]
    
    for description, command in reversal_commands:
        print(f"• {description}: {command}")
    
    print("\n⚠️  Irreversible operations:")
    irreversible_ops = [
        "DeleteModel (data loss)",
        "RemoveField (data loss)",
        "RunSQL without reverse_sql",
        "RunPython without reverse_code"
    ]
    
    for op in irreversible_ops:
        print(f"• {op}")

def demo_migration_best_practices():
    """Show migration best practices"""
    print("\n" + "=" * 60)
    print("DEMO: Migration Best Practices")
    print("=" * 60)
    
    practices = {
        "✅ Best Practices": [
            "Always review generated migration files",
            "Test migrations on development data",
            "Backup production database before migrations",
            "Use meaningful migration names: --name add_user_profile",
            "Keep migrations small and focused",
            "Provide reverse operations when possible",
            "Use historical models in data migrations",
            "Commit migrations with model changes"
        ],
        "❌ Common Mistakes": [
            "Editing migrations after they're applied",
            "Importing models directly in data migrations",
            "Deleting migration files from version control",
            "Skipping migration testing",
            "Making irreversible changes without backups",
            "Ignoring migration conflicts"
        ]
    }
    
    for category, items in practices.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")

def demo_practical_examples():
    """Show practical migration examples"""
    print("\n" + "=" * 60)
    print("DEMO: Practical Migration Examples")
    print("=" * 60)
    
    examples = [
        {
            "scenario": "Adding a non-null field to existing table",
            "solution": "1. Add field with default value\n2. Populate field with data migration\n3. Remove default in another migration",
            "code": '''
# Migration 1: Add field with default
migrations.AddField(
    model_name='book',
    name='slug',
    field=models.SlugField(default='temp-slug'),
)

# Migration 2: Populate field
migrations.RunPython(populate_book_slugs),

# Migration 3: Remove default
migrations.AlterField(
    model_name='book',
    name='slug',
    field=models.SlugField(),
)
'''
        },
        {
            "scenario": "Renaming a model",
            "solution": "Use RenameModel operation",
            "code": '''
migrations.RenameModel(
    old_name='OldModelName',
    new_name='NewModelName',
)
'''
        },
        {
            "scenario": "Splitting a model into two",
            "solution": "1. Create new model\n2. Data migration to copy data\n3. Remove fields from original model",
            "code": '''
# Migration 1: Create new model
migrations.CreateModel('AuthorProfile', fields=[...]),

# Migration 2: Copy data
migrations.RunPython(copy_author_profile_data),

# Migration 3: Remove old fields
migrations.RemoveField('Author', 'bio'),
migrations.RemoveField('Author', 'website'),
'''
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['scenario']}:")
        print(f"   Solution: {example['solution']}")
        print(f"   Code example:")
        print(example['code'])

def demo_troubleshooting():
    """Show common migration problems and solutions"""
    print("\n" + "=" * 60)
    print("DEMO: Troubleshooting Migrations")
    print("=" * 60)
    
    problems = [
        {
            "error": "Migration conflicts (duplicate numbers)",
            "cause": "Multiple developers created migrations simultaneously",
            "solution": "python manage.py makemigrations --merge"
        },
        {
            "error": "Table already exists",
            "cause": "Database table created outside of migrations",
            "solution": "python manage.py migrate --fake-initial"
        },
        {
            "error": "Cannot reverse irreversible migration",
            "cause": "Migration contains irreversible operations",
            "solution": "Restore from backup or write custom reverse operations"
        },
        {
            "error": "Foreign key constraint fails",
            "cause": "Missing dependencies or wrong migration order",
            "solution": "Check and fix migration dependencies"
        }
    ]
    
    print("\n🔧 Common problems and solutions:")
    for i, problem in enumerate(problems, 1):
        print(f"\n{i}. Error: {problem['error']}")
        print(f"   Cause: {problem['cause']}")
        print(f"   Solution: {problem['solution']}")

def run_complete_demo():
    """Run the complete interactive demo"""
    print("Django Migrations Tutorial - Interactive Demo")
    print("=" * 60)
    print("Based on: https://docs.djangoproject.com/en/5.2/topics/migrations/")
    print("=" * 60)
    
    # Show current status
    show_migration_status()
    
    # Run all demonstrations
    demo_initial_migration()
    demo_applying_migrations()
    demo_sql_migration()
    demo_model_changes()
    demo_data_migration_example()
    demo_migration_dependencies()
    demo_reversing_migrations()
    demo_migration_best_practices()
    demo_practical_examples()
    demo_troubleshooting()
    
    print(f"\n🎉 Interactive Migrations Demo Complete!")
    print(f"\n📚 What you learned:")
    print(f"  • How to create and apply migrations")
    print(f"  • Different types of migrations (schema and data)")
    print(f"  • Migration dependencies and order")
    print(f"  • How to reverse migrations")
    print(f"  • Best practices and troubleshooting")
    
    print(f"\n🔗 Try these commands yourself:")
    print(f"  • python manage.py makemigrations library")
    print(f"  • python manage.py migrate")
    print(f"  • python manage.py showmigrations")
    print(f"  • python manage.py sqlmigrate library 0001")

# Auto-run the demo
if __name__ == "__main__":
    run_complete_demo()
else:
    # When imported, just run the demo
    run_complete_demo()
