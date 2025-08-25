#!/usr/bin/env python
"""
Django Migrations Tutorial Demo Script

This script demonstrates all the concepts from the Django migrations tutorial:
https://docs.djangoproject.com/en/5.2/topics/migrations/

This tutorial covers:
1. Basic migration commands
2. Migration workflow
3. Schema changes
4. Data migrations
5. Migration dependencies
6. Reversing migrations
7. Squashing migrations
8. Migration best practices
"""

import os
import sys
import django
import subprocess
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from django.apps import apps
from blog.models import *

def run_command(command, description):
    """Helper function to run Django management commands"""
    print(f"\n🔧 {description}")
    print(f"Command: {command}")
    print("-" * 50)
    
    try:
        # Split command into parts
        cmd_parts = command.split()
        if cmd_parts[0] == 'python' and cmd_parts[1] == 'manage.py':
            # Use Django's call_command for management commands
            call_command(*cmd_parts[2:])
        else:
            # Use subprocess for other commands
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("Error:", result.stderr)
    except Exception as e:
        print(f"Command failed: {e}")
    
    print("-" * 50)

def demo_migration_commands():
    """Demonstrate the basic migration commands"""
    print("=" * 60)
    print("1. BASIC MIGRATION COMMANDS")
    print("=" * 60)
    
    print("\n📚 Django provides several migration commands:")
    print("• makemigrations - Create new migrations based on model changes")
    print("• migrate - Apply migrations to the database")
    print("• sqlmigrate - Show SQL for a specific migration")
    print("• showmigrations - List migrations and their status")
    
    # Show current migration status
    print("\n🔍 Current migration status:")
    run_command("python manage.py showmigrations", "Show all migrations")
    
    # Show SQL for a migration
    print("\n🔍 SQL for blog's initial migration:")
    run_command("python manage.py sqlmigrate blog 0001", "Show SQL for blog.0001_initial")

def demo_making_migrations():
    """Demonstrate creating new migrations"""
    print("\n" + "=" * 60)
    print("2. CREATING NEW MIGRATIONS")
    print("=" * 60)
    
    print("\n📝 Creating a new model to demonstrate migrations...")
    
    # Create a new model file
    new_model_code = '''
# Add this to your models.py for demonstration
class Author(models.Model):
    """A simple author model for migration demo"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """A simple book model for migration demo"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    pages = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
'''
    
    print("New models to add:")
    print(new_model_code)
    
    print("\n📋 After adding new models, you would run:")
    print("python manage.py makemigrations")
    print("python manage.py migrate")
    
    print("\n💡 Migration workflow:")
    print("1. Modify your models")
    print("2. Run makemigrations to create migration files")
    print("3. Review the generated migration files")
    print("4. Run migrate to apply changes to database")
    print("5. Commit both model changes and migration files to version control")

def demo_schema_changes():
    """Demonstrate various schema changes"""
    print("\n" + "=" * 60)
    print("3. SCHEMA CHANGE EXAMPLES")
    print("=" * 60)
    
    schema_examples = [
        {
            "change": "Add a field",
            "before": "class Person(models.Model):\n    first_name = models.CharField(max_length=30)\n    last_name = models.CharField(max_length=30)",
            "after": "class Person(models.Model):\n    first_name = models.CharField(max_length=30)\n    last_name = models.CharField(max_length=30)\n    email = models.EmailField()  # New field",
            "migration": "migrations.AddField('Person', 'email', models.EmailField())"
        },
        {
            "change": "Remove a field",
            "before": "class Person(models.Model):\n    first_name = models.CharField(max_length=30)\n    last_name = models.CharField(max_length=30)\n    middle_name = models.CharField(max_length=30)",
            "after": "class Person(models.Model):\n    first_name = models.CharField(max_length=30)\n    last_name = models.CharField(max_length=30)\n    # middle_name removed",
            "migration": "migrations.RemoveField('Person', 'middle_name')"
        },
        {
            "change": "Alter a field",
            "before": "class Person(models.Model):\n    name = models.CharField(max_length=50)",
            "after": "class Person(models.Model):\n    name = models.CharField(max_length=100)  # Increased length",
            "migration": "migrations.AlterField('Person', 'name', models.CharField(max_length=100))"
        },
        {
            "change": "Rename a field",
            "before": "class Person(models.Model):\n    full_name = models.CharField(max_length=100)",
            "after": "class Person(models.Model):\n    name = models.CharField(max_length=100)  # Renamed from full_name",
            "migration": "migrations.RenameField('Person', 'full_name', 'name')"
        }
    ]
    
    for i, example in enumerate(schema_examples, 1):
        print(f"\n{i}. {example['change']}:")
        print("   Before:")
        print(f"   {example['before']}")
        print("   After:")
        print(f"   {example['after']}")
        print("   Generated migration operation:")
        print(f"   {example['migration']}")

def demo_data_migrations():
    """Demonstrate data migrations"""
    print("\n" + "=" * 60)
    print("4. DATA MIGRATIONS")
    print("=" * 60)
    
    print("\n📊 Data migrations are used to modify existing data in the database.")
    print("They are separate from schema migrations and use the RunPython operation.")
    
    data_migration_example = '''
# Example data migration file
from django.db import migrations

def combine_names(apps, schema_editor):
    """Combine first_name and last_name into full_name field"""
    # Use historical models
    Person = apps.get_model("blog", "Person")
    for person in Person.objects.all():
        person.full_name = f"{person.first_name} {person.last_name}"
        person.save()

def reverse_combine_names(apps, schema_editor):
    """Reverse operation - split full_name back to first/last"""
    Person = apps.get_model("blog", "Person")
    for person in Person.objects.all():
        names = person.full_name.split(' ', 1)
        person.first_name = names[0]
        person.last_name = names[1] if len(names) > 1 else ''
        person.save()

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_person_full_name'),  # Depends on schema migration
    ]

    operations = [
        migrations.RunPython(combine_names, reverse_combine_names),
    ]
'''
    
    print("\nExample data migration:")
    print(data_migration_example)
    
    print("\n💡 Data migration best practices:")
    print("• Use historical models (apps.get_model) instead of importing models directly")
    print("• Provide reverse operations when possible")
    print("• Keep data migrations separate from schema migrations")
    print("• Test data migrations thoroughly")
    print("• Consider performance for large datasets")

def demo_migration_dependencies():
    """Demonstrate migration dependencies"""
    print("\n" + "=" * 60)
    print("5. MIGRATION DEPENDENCIES")
    print("=" * 60)
    
    print("\n🔗 Migration dependencies ensure migrations run in the correct order.")
    
    dependency_example = '''
class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),          # Depends on blog app migration
        ('auth', '0012_alter_user_first_name'),  # Depends on Django's auth app
        ('myapp', '0003_remove_old_field'), # Depends on another app
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('content', models.TextField()),
                ('author', models.ForeignKey('auth.User', on_delete=models.CASCADE)),
                ('post', models.ForeignKey('blog.Post', on_delete=models.CASCADE)),
            ],
        ),
    ]
'''
    
    print("Example migration with dependencies:")
    print(dependency_example)
    
    print("\n📋 Types of dependencies:")
    print("• Same app dependencies: Ensure migrations in the same app run in order")
    print("• Cross-app dependencies: Required when referencing models from other apps")
    print("• Swappable dependencies: For models that can be swapped (like User model)")
    
    print("\n⚠️  Dependency considerations:")
    print("• Apps without migrations cannot have relations to apps with migrations")
    print("• Circular dependencies should be avoided")
    print("• Django automatically detects most dependencies")

def demo_reversing_migrations():
    """Demonstrate reversing migrations"""
    print("\n" + "=" * 60)
    print("6. REVERSING MIGRATIONS")
    print("=" * 60)
    
    print("\n⏪ Migrations can be reversed to undo changes.")
    
    print("\n📋 Reversing migration examples:")
    print("# Reverse to specific migration:")
    print("python manage.py migrate blog 0002")
    print("")
    print("# Reverse all migrations for an app:")
    print("python manage.py migrate blog zero")
    print("")
    print("# Check what would be reversed (dry run):")
    print("python manage.py migrate --plan blog 0001")
    
    print("\n⚠️  Irreversible operations:")
    irreversible_ops = [
        "DeleteModel - Cannot recreate deleted model",
        "RemoveField - Data in removed field is lost",
        "RunSQL - Custom SQL without reverse SQL",
        "RunPython - Python code without reverse function"
    ]
    
    for op in irreversible_ops:
        print(f"• {op}")
    
    print("\n💡 Making operations reversible:")
    reversible_example = '''
# Reversible RunPython
migrations.RunPython(
    code=forward_function,
    reverse_code=reverse_function  # Provide reverse operation
)

# Reversible RunSQL
migrations.RunSQL(
    sql="CREATE INDEX idx_name ON table_name (column_name);",
    reverse_sql="DROP INDEX idx_name;"  # Provide reverse SQL
)
'''
    print(reversible_example)

def demo_migration_workflow():
    """Demonstrate the complete migration workflow"""
    print("\n" + "=" * 60)
    print("7. MIGRATION WORKFLOW")
    print("=" * 60)
    
    workflow_steps = [
        {
            "step": "1. Development",
            "actions": [
                "Modify models in models.py",
                "Run makemigrations to create migration files",
                "Review generated migration files",
                "Test migrations on development database",
                "Run migrate to apply changes"
            ]
        },
        {
            "step": "2. Version Control",
            "actions": [
                "Commit model changes and migration files together",
                "Never edit migration files after committing",
                "Include meaningful commit messages",
                "Tag releases that include schema changes"
            ]
        },
        {
            "step": "3. Collaboration",
            "actions": [
                "Pull latest changes from repository",
                "Run migrate to apply new migrations",
                "Resolve migration conflicts if they occur",
                "Communicate breaking changes to team"
            ]
        },
        {
            "step": "4. Deployment",
            "actions": [
                "Backup production database before deployment",
                "Run migrate on staging environment first",
                "Test application thoroughly on staging",
                "Deploy to production with migration step",
                "Monitor application after deployment"
            ]
        }
    ]
    
    for workflow in workflow_steps:
        print(f"\n{workflow['step']}:")
        for action in workflow['actions']:
            print(f"   • {action}")

def demo_migration_best_practices():
    """Demonstrate migration best practices"""
    print("\n" + "=" * 60)
    print("8. MIGRATION BEST PRACTICES")
    print("=" * 60)
    
    practices = {
        "✅ DO": [
            "Always backup your database before running migrations in production",
            "Test migrations on a copy of production data",
            "Review generated migration files before applying them",
            "Use meaningful names for migrations: --name descriptive_name",
            "Keep migrations small and focused",
            "Use data migrations for complex data transformations",
            "Provide reverse operations when possible",
            "Use historical models in data migrations",
            "Squash migrations periodically to reduce clutter"
        ],
        "❌ DON'T": [
            "Edit migration files after they've been applied in production",
            "Delete migration files that have been applied",
            "Mix schema and data changes in the same migration",
            "Import models directly in data migrations",
            "Ignore migration conflicts",
            "Skip testing migrations",
            "Make irreversible changes without careful consideration",
            "Forget to commit migration files",
            "Apply untested migrations to production"
        ]
    }
    
    for category, items in practices.items():
        print(f"\n{category}:")
        for item in items:
            print(f"   • {item}")

def demo_troubleshooting():
    """Demonstrate common migration issues and solutions"""
    print("\n" + "=" * 60)
    print("9. TROUBLESHOOTING MIGRATIONS")
    print("=" * 60)
    
    issues = [
        {
            "problem": "Migration conflicts (same migration number)",
            "solution": "Run 'makemigrations --merge' to create a merge migration",
            "prevention": "Pull latest changes before creating new migrations"
        },
        {
            "problem": "Fake migration already applied",
            "solution": "Use 'migrate --fake-initial' for initial migrations",
            "prevention": "Create migrations before creating database tables"
        },
        {
            "problem": "Cannot reverse irreversible migration",
            "solution": "Provide reverse operations or restore from backup",
            "prevention": "Always provide reverse operations when possible"
        },
        {
            "problem": "Migration takes too long on large tables",
            "solution": "Use database-specific tools or break into smaller migrations",
            "prevention": "Test migrations on production-sized datasets"
        },
        {
            "problem": "Foreign key constraint errors",
            "solution": "Check migration dependencies and order",
            "prevention": "Ensure proper migration dependencies"
        }
    ]
    
    print("\n🔧 Common issues and solutions:")
    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. Problem: {issue['problem']}")
        print(f"   Solution: {issue['solution']}")
        print(f"   Prevention: {issue['prevention']}")

def demo_advanced_concepts():
    """Demonstrate advanced migration concepts"""
    print("\n" + "=" * 60)
    print("10. ADVANCED MIGRATION CONCEPTS")
    print("=" * 60)
    
    print("\n🚀 Advanced migration features:")
    
    # Squashing migrations
    print("\n1. Squashing Migrations:")
    print("   Purpose: Combine multiple migrations into a single migration file")
    print("   Command: python manage.py squashmigrations myapp 0001 0004")
    print("   Benefits: Faster initial setup, cleaner migration history")
    
    # Custom migration operations
    print("\n2. Custom Migration Operations:")
    custom_op_example = '''
from django.db import migrations

class LoadFixtureOperation(migrations.Operation):
    reversible = True
    
    def __init__(self, fixture_name):
        self.fixture_name = fixture_name
    
    def state_forwards(self, app_label, state):
        # No model state changes
        pass
    
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        # Load fixture data
        call_command('loaddata', self.fixture_name)
    
    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        # Remove fixture data (implementation depends on your needs)
        pass
'''
    print("   Custom operation example:")
    print(custom_op_example)
    
    # Non-atomic migrations
    print("\n3. Non-atomic Migrations:")
    print("   Use case: When you need migrations to run outside transactions")
    print("   Example: Adding indexes on large tables in PostgreSQL")
    nonatomic_example = '''
class Migration(migrations.Migration):
    atomic = False  # Disable transaction for this migration
    
    operations = [
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY idx_name ON table_name (column_name);",
            reverse_sql="DROP INDEX idx_name;"
        ),
    ]
'''
    print("   Example:")
    print(nonatomic_example)

def demo_database_specific_considerations():
    """Demonstrate database-specific migration considerations"""
    print("\n" + "=" * 60)
    print("11. DATABASE-SPECIFIC CONSIDERATIONS")
    print("=" * 60)
    
    db_info = {
        "SQLite": {
            "strengths": ["Simple setup", "Good for development"],
            "limitations": [
                "Limited ALTER TABLE support",
                "No concurrent migrations",
                "Slower for complex operations",
                "Not recommended for production"
            ],
            "notes": "Django emulates missing features by recreating tables"
        },
        "PostgreSQL": {
            "strengths": [
                "Full migration support",
                "Transactional DDL",
                "Advanced features support",
                "Best choice for production"
            ],
            "limitations": ["Requires proper setup"],
            "notes": "Most capable database for Django migrations"
        },
        "MySQL": {
            "strengths": ["Widely supported", "Good performance"],
            "limitations": [
                "No transactional DDL",
                "Limited index size",
                "Migration failures require manual cleanup"
            ],
            "notes": "MySQL 8.0 improved DDL performance significantly"
        }
    }
    
    for db, info in db_info.items():
        print(f"\n📊 {db}:")
        print("   Strengths:")
        for strength in info["strengths"]:
            print(f"     ✅ {strength}")
        if info["limitations"]:
            print("   Limitations:")
            for limitation in info["limitations"]:
                print(f"     ⚠️  {limitation}")
        print(f"   Notes: {info['notes']}")

def demo_production_migration_strategy():
    """Demonstrate production migration strategies"""
    print("\n" + "=" * 60)
    print("12. PRODUCTION MIGRATION STRATEGY")
    print("=" * 60)
    
    strategies = [
        {
            "strategy": "Blue-Green Deployment",
            "description": "Deploy to parallel environment, then switch traffic",
            "pros": ["Zero downtime", "Easy rollback", "Full testing possible"],
            "cons": ["Requires double resources", "Complex setup"]
        },
        {
            "strategy": "Rolling Deployment",
            "description": "Update servers one by one",
            "pros": ["Gradual rollout", "Resource efficient"],
            "cons": ["Temporary inconsistency", "Complex migration coordination"]
        },
        {
            "strategy": "Maintenance Window",
            "description": "Schedule downtime for migrations",
            "pros": ["Simple and safe", "Full control"],
            "cons": ["Service interruption", "User impact"]
        },
        {
            "strategy": "Backward Compatible Migrations",
            "description": "Ensure migrations work with old and new code",
            "pros": ["No downtime", "Gradual migration"],
            "cons": ["More complex planning", "Longer migration process"]
        }
    ]
    
    print("\n🏭 Production migration strategies:")
    for i, strategy in enumerate(strategies, 1):
        print(f"\n{i}. {strategy['strategy']}:")
        print(f"   Description: {strategy['description']}")
        print("   Pros:")
        for pro in strategy['pros']:
            print(f"     ✅ {pro}")
        print("   Cons:")
        for con in strategy['cons']:
            print(f"     ⚠️  {con}")

def main():
    """Run all migration demonstrations"""
    print("Django Migrations Tutorial - Comprehensive Guide")
    print("=" * 60)
    print("Based on: https://docs.djangoproject.com/en/5.2/topics/migrations/")
    print("=" * 60)
    
    demo_migration_commands()
    demo_making_migrations()
    demo_schema_changes()
    demo_data_migrations()
    demo_migration_dependencies()
    demo_reversing_migrations()
    demo_migration_workflow()
    demo_migration_best_practices()
    demo_troubleshooting()
    demo_advanced_concepts()
    demo_database_specific_considerations()
    demo_production_migration_strategy()
    
    print(f"\n🎉 Django Migrations Tutorial Complete!")
    print(f"\n📚 Key takeaways:")
    print(f"  • Migrations are version control for your database schema")
    print(f"  • Always test migrations before applying to production")
    print(f"  • Use data migrations for complex data transformations")
    print(f"  • Provide reverse operations when possible")
    print(f"  • Follow the proper workflow: modify → makemigrations → migrate")
    print(f"  • Consider database-specific limitations")
    print(f"  • Plan production migration strategy carefully")
    
    print(f"\n🔗 Next steps:")
    print(f"  • Practice creating migrations with your own models")
    print(f"  • Set up a staging environment for testing")
    print(f"  • Learn about your database's specific features")
    print(f"  • Explore advanced migration operations")

if __name__ == "__main__":
    main()
