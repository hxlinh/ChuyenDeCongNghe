# Django Migrations Tutorial

## Overview

This comprehensive tutorial demonstrates Django's migration system based on the official documentation at: https://docs.djangoproject.com/en/5.2/topics/migrations/

Migrations are Django's way of propagating changes you make to your models into your database schema. They're designed to be mostly automatic, but you need to know when to make migrations, when to run them, and how to handle common problems.

## Table of Contents

1. [Basic Concepts](#basic-concepts)
2. [Migration Commands](#migration-commands)
3. [Workflow](#workflow)
4. [Schema Changes](#schema-changes)
5. [Data Migrations](#data-migrations)
6. [Dependencies](#dependencies)
7. [Reversing Migrations](#reversing-migrations)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Topics](#advanced-topics)

## Basic Concepts

### What are Migrations?

Migrations are version control for your database schema. They allow you to:
- Track changes to your models over time
- Apply these changes consistently across different environments
- Share database schema changes with your team
- Roll back changes when needed

### Key Components

- **Migration Files**: Python files that describe database changes
- **Migration History**: Record of which migrations have been applied
- **Operations**: Individual changes like creating tables, adding fields, etc.
- **Dependencies**: Order in which migrations must be applied

## Migration Commands

### Core Commands

#### `makemigrations`
Creates new migration files based on model changes:
```bash
# Create migrations for all apps
python manage.py makemigrations

# Create migrations for specific app
python manage.py makemigrations myapp

# Create migration with custom name
python manage.py makemigrations --name add_user_profile myapp

# Create empty migration for data migration
python manage.py makemigrations --empty myapp
```

#### `migrate`
Applies migrations to the database:
```bash
# Apply all pending migrations
python manage.py migrate

# Apply migrations for specific app
python manage.py migrate myapp

# Apply migrations up to specific migration
python manage.py migrate myapp 0003

# Reverse all migrations for an app
python manage.py migrate myapp zero
```

#### `sqlmigrate`
Shows SQL that would be executed for a migration:
```bash
python manage.py sqlmigrate myapp 0001
```

#### `showmigrations`
Lists migrations and their status:
```bash
# Show all migrations
python manage.py showmigrations

# Show migrations for specific app
python manage.py showmigrations myapp

# Show in plan format
python manage.py showmigrations --plan
```

## Workflow

### Development Workflow

1. **Modify Models**: Make changes to your `models.py` files
2. **Create Migration**: Run `makemigrations` to create migration files
3. **Review Migration**: Check the generated migration file
4. **Apply Migration**: Run `migrate` to apply changes to database
5. **Test**: Verify that everything works as expected
6. **Commit**: Commit both model changes and migration files

### Example Workflow

```python
# 1. Add a new field to your model
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()  # New field added

# 2. Create migration
# $ python manage.py makemigrations
# Migrations for 'library':
#   library/migrations/0002_author_bio.py
#     - Add field bio to author

# 3. Apply migration
# $ python manage.py migrate
# Operations to perform:
#   Apply all migrations: library
# Running migrations:
#   Applying library.0002_author_bio... OK
```

## Schema Changes

### Common Schema Operations

#### Adding Fields

```python
# Before
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

# After
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)  # New field
```

Generated migration:
```python
operations = [
    migrations.AddField(
        model_name='book',
        name='isbn',
        field=models.CharField(max_length=13, default=''),
    ),
]
```

#### Removing Fields

```python
# Migration to remove field
operations = [
    migrations.RemoveField(
        model_name='book',
        name='old_field',
    ),
]
```

#### Altering Fields

```python
# Change field properties
operations = [
    migrations.AlterField(
        model_name='book',
        name='title',
        field=models.CharField(max_length=300),  # Increased from 200
    ),
]
```

#### Renaming Fields

```python
# Rename a field
operations = [
    migrations.RenameField(
        model_name='book',
        old_name='author',
        new_name='author_name',
    ),
]
```

### Adding Non-Null Fields to Existing Tables

When adding a non-null field to a table with existing data:

```python
# Option 1: Add with default value
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='book',
            name='publication_date',
            field=models.DateField(default=date.today),
        ),
    ]

# Option 2: Multi-step approach
# Step 1: Add nullable field
migrations.AddField(
    model_name='book',
    name='publication_date',
    field=models.DateField(null=True),
)

# Step 2: Populate field with data migration
migrations.RunPython(populate_publication_dates),

# Step 3: Make field non-nullable
migrations.AlterField(
    model_name='book',
    name='publication_date',
    field=models.DateField(),
)
```

## Data Migrations

Data migrations modify existing data rather than schema structure.

### Creating Data Migrations

```bash
# Create empty migration for data changes
python manage.py makemigrations --empty myapp
```

### Data Migration Example

```python
from django.db import migrations

def populate_slugs(apps, schema_editor):
    """Generate slugs for existing books"""
    Book = apps.get_model("library", "Book")
    from django.utils.text import slugify
    
    for book in Book.objects.all():
        if not book.slug:
            book.slug = slugify(book.title)
            book.save()

def reverse_populate_slugs(apps, schema_editor):
    """Clear slugs (reverse operation)"""
    Book = apps.get_model("library", "Book")
    Book.objects.all().update(slug='')

class Migration(migrations.Migration):
    dependencies = [
        ('library', '0002_book_slug'),
    ]

    operations = [
        migrations.RunPython(
            populate_slugs,
            reverse_populate_slugs
        ),
    ]
```

### Data Migration Best Practices

1. **Use Historical Models**: Always use `apps.get_model()` instead of importing models directly
2. **Provide Reverse Operations**: Include reverse functions when possible
3. **Handle Large Datasets**: Consider batching for performance
4. **Test Thoroughly**: Test with realistic data volumes

```python
def batch_update_example(apps, schema_editor):
    """Example of batched data migration"""
    Book = apps.get_model("library", "Book")
    
    batch_size = 1000
    books = Book.objects.all()
    
    for i in range(0, books.count(), batch_size):
        batch = books[i:i + batch_size]
        for book in batch:
            book.processed = True
            book.save()
```

## Dependencies

### Understanding Dependencies

Dependencies ensure migrations run in the correct order:

```python
class Migration(migrations.Migration):
    dependencies = [
        ('library', '0001_initial'),        # Previous migration in same app
        ('auth', '0012_alter_user_first_name'),  # Django auth migration
        ('blog', '0001_initial'),           # Another app's migration
    ]
```

### Types of Dependencies

1. **Sequential Dependencies**: Previous migration in same app
2. **Cross-App Dependencies**: Migrations from other apps
3. **Swappable Dependencies**: For swappable models like User

### Swappable Dependencies

```python
from django.db import migrations
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    
    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
```

## Reversing Migrations

### Basic Reversal

```bash
# Reverse to specific migration
python manage.py migrate myapp 0002

# Reverse all migrations
python manage.py migrate myapp zero

# Show what would be reversed (dry run)
python manage.py migrate --plan myapp 0001
```

### Making Operations Reversible

#### Reversible RunPython

```python
migrations.RunPython(
    code=forward_function,
    reverse_code=reverse_function
)
```

#### Reversible RunSQL

```python
migrations.RunSQL(
    sql="CREATE INDEX idx_name ON table_name (column);",
    reverse_sql="DROP INDEX idx_name;"
)
```

### Irreversible Operations

Some operations cannot be automatically reversed:
- `DeleteModel` (data loss)
- `RemoveField` (data loss)
- `RunSQL` without reverse SQL
- `RunPython` without reverse function

```python
# Mark migration as irreversible
from django.db import migrations

class Migration(migrations.Migration):
    operations = [
        migrations.RunSQL(
            "DROP TABLE old_table;",
            reverse_sql=migrations.RunSQL.noop  # Cannot be reversed
        ),
    ]
```

## Best Practices

### Development Best Practices

✅ **DO**:
- Review all generated migration files
- Test migrations on development data
- Use meaningful migration names
- Keep migrations small and focused
- Backup production database before migrations
- Provide reverse operations when possible
- Use historical models in data migrations

❌ **DON'T**:
- Edit migrations after they're applied
- Delete migration files from version control
- Import models directly in data migrations
- Skip migration testing
- Apply untested migrations to production

### Production Deployment

#### Pre-deployment Checklist
- [ ] Backup production database
- [ ] Test migrations on staging environment
- [ ] Review all migration files
- [ ] Check for breaking changes
- [ ] Plan rollback strategy

#### Deployment Strategies

1. **Maintenance Window**
   ```bash
   # Take application offline
   python manage.py migrate
   # Bring application online
   ```

2. **Zero-Downtime Deployment**
   - Use backward-compatible migrations
   - Deploy in multiple phases
   - Coordinate with application deployment

3. **Blue-Green Deployment**
   - Deploy to parallel environment
   - Switch traffic after verification

### Version Control

```bash
# Commit migrations with model changes
git add myapp/models.py myapp/migrations/0002_*.py
git commit -m "Add user profile model with email field"

# Tag releases with schema changes
git tag -a v1.2.0 -m "Release with new user profile model"
```

## Troubleshooting

### Common Issues and Solutions

#### Migration Conflicts

**Problem**: Multiple developers create migrations with same number
```
CommandError: Conflicting migrations detected
```

**Solution**: Merge migrations
```bash
python manage.py makemigrations --merge
```

#### Table Already Exists

**Problem**: Database table exists but migration thinks it needs to create it
```
django.db.utils.OperationalError: table "myapp_mymodel" already exists
```

**Solution**: Fake the initial migration
```bash
python manage.py migrate --fake-initial
```

#### Cannot Reverse Migration

**Problem**: Trying to reverse irreversible migration
```
django.db.migrations.exceptions.IrreversibleError
```

**Solution**: 
- Restore from backup
- Write custom reverse operations
- Use `--fake` to mark as reversed without changing database

#### Foreign Key Constraint Fails

**Problem**: Migration tries to create foreign key to non-existent table
```
django.db.utils.IntegrityError: FOREIGN KEY constraint failed
```

**Solution**: Check migration dependencies
```python
dependencies = [
    ('otherapp', '0001_initial'),  # Ensure referenced app migrated first
]
```

### Debugging Migrations

#### Check Migration Status
```bash
python manage.py showmigrations --verbosity=2
```

#### View Migration Plan
```bash
python manage.py migrate --plan
```

#### Dry Run Migration
```bash
python manage.py migrate --verbosity=2 --dry-run
```

#### Check SQL Output
```bash
python manage.py sqlmigrate myapp 0001
```

## Advanced Topics

### Custom Migration Operations

```python
from django.db import migrations

class LoadDataOperation(migrations.Operation):
    reversible = True
    
    def __init__(self, fixture_name):
        self.fixture_name = fixture_name
    
    def state_forwards(self, app_label, state):
        # No model state changes
        pass
    
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        # Load fixture
        from django.core.management import call_command
        call_command('loaddata', self.fixture_name)
    
    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        # Remove data (implement as needed)
        pass
```

### Non-Atomic Migrations

For operations that cannot run in transactions:

```python
class Migration(migrations.Migration):
    atomic = False  # Disable transaction
    
    operations = [
        migrations.RunSQL(
            "CREATE INDEX CONCURRENTLY idx_name ON table_name (column);",
            reverse_sql="DROP INDEX idx_name;"
        ),
    ]
```

### Squashing Migrations

Combine multiple migrations into one:

```bash
python manage.py squashmigrations myapp 0001 0004
```

Benefits:
- Faster initial setup for new environments
- Cleaner migration history
- Reduced migration files

Process:
1. Create squashed migration
2. Test thoroughly
3. Deploy squashed migration
4. Remove original migrations after all environments updated

### Database-Specific Considerations

#### SQLite
- Limited ALTER TABLE support
- Django recreates tables for complex changes
- Good for development, not production

#### PostgreSQL
- Full transactional DDL support
- Best migration support
- Recommended for production

#### MySQL
- No transactional DDL
- Manual cleanup required on migration failure
- Index size limitations

## Running the Tutorial

### Interactive Demo

```bash
cd lab2_models_tutorial
python manage.py shell
>>> exec(open('migrations_interactive_demo.py').read())
```

### Step-by-Step Practice

1. **Create New App**:
   ```bash
   python manage.py startapp tutorial_app
   ```

2. **Add Models**:
   ```python
   # tutorial_app/models.py
   class Author(models.Model):
       name = models.CharField(max_length=100)
   ```

3. **Create Migration**:
   ```bash
   python manage.py makemigrations tutorial_app
   ```

4. **Apply Migration**:
   ```bash
   python manage.py migrate
   ```

5. **Modify Model**:
   ```python
   class Author(models.Model):
       name = models.CharField(max_length=100)
       email = models.EmailField()  # New field
   ```

6. **Create and Apply New Migration**:
   ```bash
   python manage.py makemigrations tutorial_app
   python manage.py migrate
   ```

## Summary

Django migrations provide a robust system for managing database schema changes:

- **Automatic**: Django detects model changes and generates migrations
- **Version Controlled**: Migration files track all schema changes
- **Reversible**: Most operations can be undone
- **Collaborative**: Team members share schema changes through version control
- **Production-Ready**: Suitable for deployment to production environments

Key principles:
1. Always review generated migrations
2. Test thoroughly before production
3. Use data migrations for complex data transformations
4. Follow the proper workflow: modify → makemigrations → migrate
5. Backup before major migrations

The migration system is one of Django's most powerful features for maintaining database consistency across development, staging, and production environments.

---

**Resources:**
- [Django Migrations Documentation](https://docs.djangoproject.com/en/5.2/topics/migrations/)
- [Migration Operations Reference](https://docs.djangoproject.com/en/5.2/ref/migration-operations/)
- [Writing Migrations](https://docs.djangoproject.com/en/5.2/howto/writing-migrations/)
