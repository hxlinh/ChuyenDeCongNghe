# Django Queries Tutorial

## Overview

This tutorial demonstrates the comprehensive Django database query capabilities following the official Django documentation at: https://docs.djangoproject.com/en/5.2/topics/db/queries/

## Tutorial Structure

### Prerequisites
- Django 5.2.5 installed
- SQLite database (default)
- Basic understanding of Django models
- Previous completion of Django Models Tutorial

### Models Used

The tutorial uses the following models from our `blog` app:

```python
# Musician and Album (Many-to-One relationship)
class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()

# Student (Field options and choices)
class Student(models.Model):
    YEAR_IN_SCHOOL_CHOICES = [
        ("FR", "Freshman"),
        ("SO", "Sophomore"),
        ("JR", "Junior"),
        ("SR", "Senior"),
        ("GR", "Graduate"),
    ]
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year_in_school = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    graduation_year = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
```

## Key Concepts Demonstrated

### 1. Basic Queries

#### Object Retrieval
```python
# Get a single object
john = Musician.objects.get(first_name="John")

# Handle exceptions
try:
    musician = Musician.objects.get(first_name="John")
except Musician.DoesNotExist:
    print("Musician not found")
except Musician.MultipleObjectsReturned:
    print("Multiple musicians found")
```

#### Filtering
```python
# Basic filtering
guitarists = Musician.objects.filter(instrument__icontains="Guitar")

# Chaining filters
recent_albums = Album.objects.filter(
    release_date__year__gte=1965
).filter(num_stars__gte=4)

# Exclude
non_guitarists = Musician.objects.exclude(instrument__icontains="Guitar")
```

### 2. Field Lookups

#### String Lookups
```python
# Exact match
five_star = Album.objects.filter(num_stars__exact=5)

# Case-insensitive contains
albums = Album.objects.filter(name__icontains="pepper")

# Starts with / ends with
albums_a = Album.objects.filter(name__istartswith="a")
albums_s = Album.objects.filter(name__endswith="s")
```

#### Date Lookups
```python
# Date ranges
sixties_albums = Album.objects.filter(
    release_date__range=(date(1960, 1, 1), date(1969, 12, 31))
)

# Year/month/day extraction
albums_1965 = Album.objects.filter(release_date__year=1965)
summer_albums = Album.objects.filter(release_date__month__in=[6, 7, 8])
```

#### Comparison Lookups
```python
# Greater than, less than
high_rated = Album.objects.filter(num_stars__gte=4)
recent = Album.objects.filter(release_date__gt=date(1970, 1, 1))

# IN queries
top_musicians = Musician.objects.filter(last_name__in=['Lennon', 'McCartney'])

# Null checks
students_with_grad = Student.objects.filter(graduation_year__isnull=False)
```

### 3. Complex Q Object Queries

#### OR Conditions
```python
from django.db.models import Q

# Simple OR
guitar_or_piano = Musician.objects.filter(
    Q(instrument__icontains="Guitar") | Q(instrument__icontains="Piano")
)

# Complex OR with AND
complex_query = Album.objects.filter(
    (Q(num_stars=5) | Q(num_stars=4)) & Q(release_date__year__gte=1965)
)
```

#### NOT Conditions
```python
# Negation
not_five_star = Album.objects.filter(~Q(num_stars=5))
```

#### Dynamic Q Construction
```python
# Building Q objects dynamically
search_terms = ["Beatles", "Dylan", "Jazz"]
q_objects = Q()
for term in search_terms:
    q_objects |= Q(name__icontains=term)

results = Album.objects.filter(q_objects)
```

### 4. F Expressions

#### Field Comparisons
```python
from django.db.models import F

# Mathematical operations
albums_calc = Album.objects.annotate(
    rating_doubled=F('num_stars') * 2,
    year_plus_rating=F('release_date__year') + F('num_stars')
)
```

#### String Operations
```python
from django.db.models.functions import Concat, Length

# String concatenation
musicians_full = Musician.objects.annotate(
    full_name=Concat('first_name', Value(' '), 'last_name'),
    name_length=Length('last_name')
)
```

### 5. Aggregation

#### Basic Aggregation
```python
from django.db.models import Count, Avg, Max, Min, Sum

# Aggregate across all records
stats = Album.objects.aggregate(
    total=Count('id'),
    avg_rating=Avg('num_stars'),
    max_rating=Max('num_stars'),
    min_rating=Min('num_stars')
)
```

#### Grouping with Annotations
```python
# Group by musician and aggregate their albums
musician_stats = Musician.objects.annotate(
    album_count=Count('album'),
    avg_rating=Avg('album__num_stars'),
    best_rating=Max('album__num_stars')
).filter(album_count__gt=0)
```

#### Conditional Aggregation
```python
from django.db.models import Case, When

# Count with conditions
student_stats = Student.objects.aggregate(
    total=Count('id'),
    undergrads=Count(Case(
        When(year_in_school__in=['FR', 'SO', 'JR', 'SR'], then=1)
    )),
    grads=Count(Case(When(year_in_school='GR', then=1)))
)
```

### 6. Ordering and Slicing

#### Multiple Field Ordering
```python
# Order by multiple fields
albums_ordered = Album.objects.order_by('-num_stars', 'release_date', 'name')

# Order by related fields
albums_by_artist = Album.objects.order_by('artist__last_name')

# Random ordering
random_albums = Album.objects.order_by('?')[:3]
```

#### Result Slicing
```python
# Limit results
top_albums = Album.objects.order_by('-num_stars')[:5]

# Pagination-style slicing
page_2 = Album.objects.all()[10:20]
```

### 7. Relationship Queries

#### Forward Relationships
```python
# Access related objects
album = Album.objects.get(name="Abbey Road")
artist_name = album.artist.first_name  # Follow ForeignKey
instrument = album.artist.instrument   # Chain relationships
```

#### Reverse Relationships
```python
# Access reverse relationships
john = Musician.objects.get(first_name="John")
john_albums = john.album_set.all()  # Reverse ForeignKey lookup
```

#### Filtering by Related Fields
```python
# Filter by related field values
guitar_albums = Album.objects.filter(artist__instrument__icontains="Guitar")
albums_by_john = Album.objects.filter(artist__first_name="John")
```

### 8. Query Optimization

#### Select Related (JOINs)
```python
# Inefficient (N+1 queries)
albums = Album.objects.all()
for album in albums:
    print(f"{album.name} by {album.artist.first_name}")  # Extra query per album

# Efficient (single query with JOIN)
albums = Album.objects.select_related('artist').all()
for album in albums:
    print(f"{album.name} by {album.artist.first_name}")  # No extra queries
```

#### Prefetch Related (for Many-to-Many)
```python
# For reverse foreign keys and many-to-many
musicians = Musician.objects.prefetch_related('album_set').all()
for musician in musicians:
    for album in musician.album_set.all():  # No extra queries
        print(album.name)
```

#### Field Selection
```python
# Only specific fields
albums_minimal = Album.objects.only('name', 'num_stars')

# Defer specific fields
albums_deferred = Album.objects.defer('release_date')
```

### 9. Advanced Features

#### Distinct Queries
```python
# Remove duplicates
instruments = Musician.objects.values_list('instrument', flat=True).distinct()
```

#### Values and Values List
```python
# Dictionary-like results
album_data = Album.objects.values('name', 'num_stars', 'artist__first_name')

# Flat list results
album_names = Album.objects.values_list('name', flat=True)
```

#### Raw SQL
```python
# Raw SQL queries
guitarists = Musician.objects.raw(
    "SELECT * FROM blog_musician WHERE instrument LIKE %s",
    ["%Guitar%"]
)

# Direct SQL execution
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM blog_album WHERE num_stars = %s", [5])
    count = cursor.fetchone()[0]
```

### 10. Database Functions

#### String Functions
```python
from django.db.models.functions import Upper, Lower, Length

musicians_processed = Musician.objects.annotate(
    name_upper=Upper('last_name'),
    name_lower=Lower('first_name'),
    name_length=Length('last_name')
)
```

#### Date Functions
```python
from django.db.models.functions import Extract, TruncYear

albums_by_year = Album.objects.annotate(
    year=Extract('release_date', 'year'),
    decade=TruncYear('release_date')
)
```

## Performance Best Practices

### 1. Query Optimization
- Use `select_related()` for ForeignKey relationships
- Use `prefetch_related()` for Many-to-Many and reverse ForeignKey
- Use `only()` and `defer()` to limit fields
- Monitor query count with `django.db.connection.queries`

### 2. Efficient Filtering
- Use database-level filtering instead of Python filtering
- Use `exists()` instead of `len()` for existence checks
- Use `count()` instead of `len()` for counting

### 3. Batch Operations
- Use `bulk_create()` for creating multiple objects
- Use `bulk_update()` for updating multiple objects
- Use `update()` for updating querysets

## Running the Tutorial

### Method 1: Interactive Django Shell
```bash
cd lab2_models_tutorial
python manage.py shell
>>> exec(open('queries_demo_interactive.py').read())
```

### Method 2: Standalone Script
```bash
cd lab2_models_tutorial
python demo_advanced_queries.py
```

### Method 3: Step by Step
```bash
cd lab2_models_tutorial
python manage.py shell
>>> from blog.models import *
>>> from django.db.models import Q, F, Count, Avg
>>> # Run individual query examples
```

## Sample Output

The tutorial demonstrates:
- Creating 10 musicians with various instruments
- Creating 12 albums with different ratings and dates
- Creating 8 students with different academic levels
- Running comprehensive query examples showing all Django ORM capabilities

## Key Learning Outcomes

After completing this tutorial, you will understand:

1. **Basic Query Operations**: Creating, reading, updating, and deleting records
2. **Advanced Filtering**: Complex conditions using Q objects and field lookups
3. **Relationship Traversal**: Working with ForeignKey and Many-to-Many relationships
4. **Aggregation and Annotation**: Calculating statistics and derived values
5. **Query Optimization**: Writing efficient queries and avoiding N+1 problems
6. **Raw SQL Integration**: When and how to use raw SQL in Django
7. **Performance Monitoring**: Tools and techniques for query performance analysis

## Next Steps

1. **Explore Django Admin**: Visit http://127.0.0.1:8001/admin/ to see the data
2. **Try Modifications**: Experiment with different query patterns
3. **Performance Analysis**: Use Django Debug Toolbar for query analysis
4. **Advanced Topics**: Explore custom managers, query expressions, and database functions

## Resources

- [Django ORM Documentation](https://docs.djangoproject.com/en/5.2/topics/db/queries/)
- [Django Model Field Reference](https://docs.djangoproject.com/en/5.2/ref/models/fields/)
- [Django QuerySet API](https://docs.djangoproject.com/en/5.2/ref/models/querysets/)
- [Database Optimization](https://docs.djangoproject.com/en/5.2/topics/db/optimization/)

---

**Tutorial completed successfully!** 🎉

The Django Queries Tutorial provides a comprehensive foundation for working with Django's powerful ORM system. Practice these concepts with your own models and data to build expertise in database operations.
