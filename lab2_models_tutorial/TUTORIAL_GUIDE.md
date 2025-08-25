# Django Models Tutorial - Complete Guide

## Overview
This document provides a comprehensive walkthrough of the Django Models tutorial from https://docs.djangoproject.com/en/5.2/topics/db/models/

## What We've Implemented

### 1. Basic Model Example
```python
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

**Key Concepts:**
- Models inherit from `django.db.models.Model`
- Each field is a class attribute representing a database column
- Django automatically creates an `id` primary key field
- The `__str__` method defines string representation

### 2. Field Types and Options

#### Field Types Examples:
- `CharField`: Text with maximum length
- `IntegerField`: Integer numbers
- `DateField`: Date values
- `BooleanField`: True/False values
- `EmailField`: Email addresses with validation
- `TextField`: Large text content

#### Field Options Examples:
```python
class Student(models.Model):
    YEAR_IN_SCHOOL_CHOICES = [
        ("FR", "Freshman"),
        ("SO", "Sophomore"),
        ("JR", "Junior"),
        ("SR", "Senior"),
        ("GR", "Graduate"),
    ]
    
    first_name = models.CharField(max_length=30)
    year_in_school = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    graduation_year = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
```

**Key Field Options:**
- `max_length`: Maximum length for character fields
- `choices`: Predefined options for a field
- `null=True`: Allows NULL values in database
- `blank=True`: Allows empty values in forms
- `unique=True`: Ensures field values are unique
- `default`: Default value for the field

### 3. Relationships

#### Many-to-One (ForeignKey)
```python
class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```

**Key Concepts:**
- `ForeignKey` creates a many-to-one relationship
- `on_delete=models.CASCADE`: Deletes albums when musician is deleted
- Access related objects via `musician.album_set.all()`

#### Many-to-Many
```python
class Topping(models.Model):
    name = models.CharField(max_length=50)

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    toppings = models.ManyToManyField(Topping)
```

**Key Concepts:**
- `ManyToManyField` creates a many-to-many relationship
- Django creates an intermediate table automatically
- Add relationships with `pizza.toppings.add(topping)`

#### Many-to-Many with Through Model
```python
class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```

**Key Concepts:**
- `through` parameter specifies custom intermediate model
- Allows additional fields on the relationship
- Create relationships by creating instances of the through model

#### One-to-One
```python
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):  # Inherits from Place
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

**Key Concepts:**
- Model inheritance creates implicit `OneToOneField`
- Access parent from child: `restaurant.place_ptr`
- Access child from parent: `place.restaurant`

### 4. Model Methods

#### Custom Instance Methods
```python
class PersonExtended(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        """Returns the person's baby-boomer status."""
        if self.birth_date < date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    @property
    def full_name(self):
        """Returns the person's full name."""
        return f"{self.first_name} {self.last_name}"
```

#### Overriding Model Methods
```python
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, **kwargs):
        # Custom logic before saving
        if self.name == "Yoko Ono's blog":
            return  # Prevent saving this specific blog
        super().save(**kwargs)  # Call the "real" save() method
```

### 5. Meta Options
```python
class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
```

**Common Meta Options:**
- `ordering`: Default ordering for queries
- `verbose_name_plural`: Plural name for admin interface
- `db_table`: Custom database table name
- `abstract = True`: Makes model abstract (no database table)

### 6. Model Inheritance

#### Abstract Base Classes
```python
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ["name"]

class StudentChild(CommonInfo):
    home_group = models.CharField(max_length=5)
```

**Key Concepts:**
- `abstract = True` prevents table creation for base class
- Child classes inherit all fields from abstract parent
- No database table for abstract models

#### Multi-table Inheritance
```python
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

**Key Concepts:**
- Each model gets its own database table
- Implicit `OneToOneField` links child to parent
- Can query both as separate models

## How to Use This Tutorial

### 1. Explore the Models
- All models are defined in `blog/models.py`
- Each model demonstrates different Django concepts
- Run the demo script: `python demo_models.py`

### 2. Admin Interface
1. Start the server: `python manage.py runserver 8001`
2. Visit: http://127.0.0.1:8001/admin/
3. Login with username: `admin` and your password
4. Explore all the models and their relationships

### 3. Django Shell
Experiment with the models in the Django shell:
```bash
python manage.py shell
```

```python
from blog.models import Person, Student, Album

# Create objects
person = Person.objects.create(first_name="John", last_name="Doe")

# Query objects
all_persons = Person.objects.all()
specific_person = Person.objects.get(first_name="John")

# Update objects
person.last_name = "Smith"
person.save()

# Delete objects
person.delete()
```

### 4. Key Django Model Features Demonstrated

1. **Field Types**: CharField, IntegerField, DateField, BooleanField, etc.
2. **Field Options**: max_length, choices, null, blank, unique, default
3. **Relationships**: ForeignKey, ManyToManyField, OneToOneField
4. **Model Methods**: Custom instance methods, properties, overriding save()
5. **Meta Options**: ordering, verbose names, abstract models
6. **Inheritance**: Abstract base classes, multi-table inheritance
7. **Constraints**: Unique constraints, foreign key constraints

### 5. Database Operations

The tutorial covers:
- Creating migrations: `python manage.py makemigrations`
- Applying migrations: `python manage.py migrate`
- Querying data using the Django ORM
- Relationships and joins
- Custom model methods and properties

## Next Steps

1. **Study the Models**: Examine each model in `blog/models.py`
2. **Run Queries**: Use the Django shell to query and manipulate data
3. **Explore Admin**: Use the admin interface to see models in action
4. **Modify Models**: Try adding new fields or relationships
5. **Read Documentation**: Visit https://docs.djangoproject.com/en/5.2/topics/db/models/

## Files Created

- `blog/models.py`: All model definitions
- `blog/admin.py`: Admin interface registration
- `demo_models.py`: Comprehensive demo script
- `blog/migrations/0001_initial.py`: Database migrations

This tutorial provides a complete implementation of the Django Models documentation with practical examples you can run and modify!
