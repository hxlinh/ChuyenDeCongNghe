# Django Initial Data Tutorial

## Overview
This tutorial demonstrates how to provide initial data for Django models using two main approaches:
1. **Data Migrations** - Programmatic approach that runs automatically
2. **Fixtures** - Static data files that can be loaded manually

Based on: https://docs.djangoproject.com/en/4.1/howto/initial-data/

## Table of Contents
1. [Understanding Initial Data](#understanding-initial-data)
2. [Method 1: Data Migrations](#method-1-data-migrations)
3. [Method 2: Fixtures](#method-2-fixtures)
4. [Comparing Approaches](#comparing-approaches)
5. [Best Practices](#best-practices)
6. [Practical Examples](#practical-examples)
7. [Testing with Initial Data](#testing-with-initial-data)
8. [Troubleshooting](#troubleshooting)

## Understanding Initial Data

Initial data is pre-populated information that you want to include in your database when setting up your Django application. This is useful for:

- **Reference data**: Categories, countries, currencies, etc.
- **Default settings**: Configuration values, user roles, permissions
- **Sample data**: For development and testing
- **System data**: Required for application functionality

## Method 1: Data Migrations

Data migrations are Python scripts that run automatically when you apply migrations. They're the recommended approach for essential data that your application needs to function.

### Advantages of Data Migrations:
- ✅ **Automatic**: Run during `migrate` command
- ✅ **Version controlled**: Part of your migration history
- ✅ **Reversible**: Can define rollback operations
- ✅ **Environment aware**: Can behave differently per environment
- ✅ **Test compatible**: Run during test database setup

### Creating a Data Migration:

```bash
# Create an empty migration
python manage.py makemigrations library --empty --name=load_initial_data
```

### Example Data Migration:

```python
from django.db import migrations
from datetime import date

def load_initial_data(apps, schema_editor):
    \"\"\"Load initial data for the library app\"\"\"
    # Get model classes (use apps.get_model, not direct imports)
    Author = apps.get_model('library', 'Author')
    Category = apps.get_model('library', 'Category')
    Book = apps.get_model('library', 'Book')
    
    # Create data with get_or_create to avoid duplicates
    author, created = Author.objects.get_or_create(
        name='Terry Pratchett',
        defaults={
            'email': 'terry.pratchett@example.com',
            'birth_date': date(1948, 4, 28),
            'bio': 'English author of fantasy novels...'
        }
    )

def reverse_initial_data(apps, schema_editor):
    \"\"\"Remove initial data (for rollback)\"\"\"
    Author = apps.get_model('library', 'Author')
    Author.objects.filter(name='Terry Pratchett').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('library', '0002_previous_migration'),
    ]
    
    operations = [
        migrations.RunPython(
            load_initial_data,
            reverse_initial_data,
        ),
    ]
```

### Key Points for Data Migrations:
- Use `apps.get_model()` instead of direct model imports
- Use `get_or_create()` to avoid duplicate data
- Always define a reverse function for rollbacks
- Be careful with foreign key relationships (create dependencies first)

## Method 2: Fixtures

Fixtures are static data files (JSON, XML, or YAML) that can be loaded manually into your database.

### Advantages of Fixtures:
- ✅ **Human readable**: Easy to edit and review
- ✅ **Language agnostic**: JSON/YAML can be used by other tools
- ✅ **Flexible**: Can be loaded selectively
- ✅ **Version control friendly**: Text files that show clear diffs

### Disadvantages of Fixtures:
- ❌ **Manual loading**: Must remember to run `loaddata`
- ❌ **Not automatic**: Don't load during migrations
- ❌ **Overwrite data**: Replace existing records with same primary key
- ❌ **Test limitations**: Only work with `TransactionTestCase.fixtures`

### Creating Fixtures

#### 1. Fixture Directory Structure:
```
library/
├── fixtures/
│   ├── initial_authors.json
│   ├── initial_categories.json
│   ├── initial_books.json
│   ├── library_sample_data.json
│   └── additional_books.yaml
```

#### 2. JSON Fixture Example:
```json
[
  {
    "model": "library.author",
    "pk": 1,
    "fields": {
      "name": "J.K. Rowling",
      "email": "jk.rowling@example.com",
      "birth_date": "1965-07-31",
      "bio": "British author best known for Harry Potter..."
    }
  },
  {
    "model": "library.book",
    "pk": 1,
    "fields": {
      "title": "Harry Potter and the Philosopher's Stone",
      "author": 1,
      "category": 1,
      "publication_date": "1997-06-26",
      "pages": 223,
      "isbn": "9780747532699",
      "price": "19.99",
      "is_available": true
    }
  }
]
```

#### 3. YAML Fixture Example:
```yaml
- model: library.author
  pk: 10
  fields:
    name: Stephen King
    email: stephen.king@example.com
    birth_date: 1947-09-21
    bio: American author of horror fiction...

- model: library.book
  pk: 10
  fields:
    title: The Shining
    author: 10
    category: 10
    publication_date: 1977-01-28
    pages: 447
    isbn: 9780307743657
    price: 18.99
    is_available: true
```

### Loading Fixtures:

```bash
# Load specific fixtures
python manage.py loaddata initial_authors
python manage.py loaddata initial_categories
python manage.py loaddata initial_books

# Load multiple fixtures at once
python manage.py loaddata initial_authors initial_categories initial_books

# Load from specific path
python manage.py loaddata library/fixtures/library_sample_data.json

# Load YAML fixtures (requires PyYAML)
python manage.py loaddata additional_books.yaml
```

### Creating Fixtures from Existing Data:

```bash
# Dump all data from an app
python manage.py dumpdata library > library_data.json

# Dump specific models
python manage.py dumpdata library.Author library.Category > authors_categories.json

# Dump with indentation (more readable)
python manage.py dumpdata library --indent 2 > library_formatted.json

# Exclude certain fields
python manage.py dumpdata library --exclude library.Review > library_no_reviews.json
```

## Comparing Approaches

| Aspect | Data Migrations | Fixtures |
|--------|----------------|----------|
| **Loading** | Automatic (during migrate) | Manual (loaddata command) |
| **Testing** | ✅ Available in all tests | ❌ Only TransactionTestCase.fixtures |
| **Rollback** | ✅ Reversible operations | ❌ No built-in rollback |
| **Dependencies** | ✅ Respects migration order | ⚠️ Manual dependency management |
| **Data Updates** | ✅ Programmatic logic | ❌ Complete replacement |
| **Environment** | ✅ Can vary by environment | ❌ Static data only |
| **Maintenance** | ⚠️ Code-based (more complex) | ✅ Simple text files |

## Best Practices

### When to Use Data Migrations:
- **Essential system data** required for application functionality
- **Reference data** that rarely changes (countries, currencies, etc.)
- **Default configurations** and settings
- **Data that needs environment-specific values**

### When to Use Fixtures:
- **Development sample data** for testing UI/UX
- **Demo data** for presentations
- **Large datasets** that are easier to manage as files
- **Data sharing** between team members

### General Best Practices:

1. **Use get_or_create()** in data migrations to avoid duplicates:
   ```python
   author, created = Author.objects.get_or_create(
       name='J.K. Rowling',
       defaults={'email': 'jk@example.com', ...}
   )
   ```

2. **Handle dependencies properly** in migrations:
   ```python
   # Create authors before books
   author = Author.objects.create(name='Author Name')
   Book.objects.create(title='Book Title', author=author)
   ```

3. **Use meaningful primary keys** in fixtures for relationships:
   ```json
   {"model": "library.book", "pk": 1, "fields": {"author": 1}}
   ```

4. **Document your fixtures** with comments and README files

5. **Keep fixtures small and focused** - separate by logical groups

6. **Version control everything** - both migrations and fixtures

## Practical Examples

### Example 1: Loading All Fixtures
```bash
# Navigate to project directory
cd lab2_models_tutorial

# Load individual fixtures in order (respecting dependencies)
python manage.py loaddata initial_authors
python manage.py loaddata initial_categories  
python manage.py loaddata initial_books
python manage.py loaddata initial_reviews

# Or load the sample data fixture
python manage.py loaddata library_sample_data

# Load YAML fixture (if PyYAML is installed)
python manage.py loaddata additional_books.yaml
```

### Example 2: Creating Custom Fixtures
```bash
# Create fixture from current data
python manage.py dumpdata library.Author --indent 2 > my_authors.json

# Load your custom fixture
python manage.py loaddata my_authors.json
```

### Example 3: Data Migration with Error Handling
```python
def load_initial_data(apps, schema_editor):
    Author = apps.get_model('library', 'Author')
    
    try:
        author, created = Author.objects.get_or_create(
            name='Test Author',
            defaults={'email': 'test@example.com'}
        )
        if created:
            print(f\"Created author: {author.name}\")
        else:
            print(f\"Author already exists: {author.name}\")
    except Exception as e:
        print(f\"Error creating author: {e}\")
        raise
```

## Testing with Initial Data

### Using Fixtures in Tests:
```python
from django.test import TransactionTestCase

class LibraryTestCase(TransactionTestCase):
    fixtures = ['initial_authors.json', 'initial_categories.json']
    
    def test_author_count(self):
        from library.models import Author
        self.assertEqual(Author.objects.count(), 4)  # From fixture
```

### Using Data Migrations in Tests:
Data migrations run automatically when the test database is created, so the data is available in all test types:

```python
from django.test import TestCase

class LibraryTestCase(TestCase):
    def test_migration_data(self):
        from library.models import Author
        # Data from migrations is automatically available
        self.assertTrue(Author.objects.filter(name='Terry Pratchett').exists())
```

## Troubleshooting

### Common Issues and Solutions:

#### 1. Foreign Key Constraint Errors
**Problem**: Loading fixtures with foreign key relationships in wrong order
```
django.db.utils.IntegrityError: FOREIGN KEY constraint failed
```

**Solution**: Load fixtures in dependency order:
```bash
# Correct order: dependencies first
python manage.py loaddata authors categories books reviews
```

#### 2. Duplicate Primary Key Errors
**Problem**: Trying to load fixture with existing primary keys
```
django.db.utils.IntegrityError: UNIQUE constraint failed
```

**Solutions**:
- Clear database: `python manage.py flush`
- Use different primary keys in fixtures
- Use `get_or_create()` in data migrations

#### 3. Fixture Not Found
**Problem**: Django can't find your fixture file
```
CommandError: No fixture named 'my_fixture' found.
```

**Solutions**:
- Check file is in `app/fixtures/` directory
- Use full path: `python manage.py loaddata app/fixtures/my_fixture.json`
- Check `FIXTURE_DIRS` setting

#### 4. Migration Data Not Available in Tests
**Problem**: Data from migrations not appearing in regular TestCase

**Solution**: Data migrations run during test database setup, so data should be available. If not:
- Check migration dependencies
- Ensure migrations have been applied: `python manage.py migrate`
- Use `TransactionTestCase` if needed

#### 5. YAML Fixture Errors
**Problem**: YAML fixtures not loading
```
CommandError: YAML serialization requires PyYAML.
```

**Solution**: Install PyYAML:
```bash
pip install PyYAML
```

### Debugging Tips:

1. **Check what fixtures Django can find**:
   ```bash
   python manage.py loaddata --verbosity=2 nonexistent
   # Shows searched directories
   ```

2. **Validate fixture format**:
   ```bash
   python -m json.tool my_fixture.json  # For JSON
   python -c \"import yaml; yaml.safe_load(open('my_fixture.yaml'))\"  # For YAML
   ```

3. **Test migrations in isolation**:
   ```bash
   python manage.py migrate library 0002  # Go to previous migration
   python manage.py migrate library 0003  # Apply your data migration
   ```

## Summary

This tutorial covered two main approaches for providing initial data in Django:

1. **Data Migrations**: Automatic, version-controlled, reversible - best for essential system data
2. **Fixtures**: Manual, human-readable, flexible - best for sample/demo data

### Key Takeaways:
- Use data migrations for critical system data that must always be present
- Use fixtures for development data, samples, and large datasets
- Always test your initial data loading process
- Document your data requirements and loading procedures
- Consider your team's workflow when choosing between approaches

### Files Created in This Tutorial:
- `library/fixtures/initial_authors.json` - Author fixture data
- `library/fixtures/initial_categories.json` - Category fixture data  
- `library/fixtures/initial_books.json` - Book fixture data
- `library/fixtures/initial_reviews.json` - Review fixture data
- `library/fixtures/library_sample_data.json` - Combined sample data
- `library/fixtures/additional_books.yaml` - YAML format example
- `library/migrations/0003_load_initial_data.py` - Data migration example

### Next Steps:
1. Practice loading different fixtures
2. Create your own data migrations
3. Experiment with `dumpdata` and `loaddata` commands
4. Integrate initial data loading into your deployment process

Happy coding! 🚀
