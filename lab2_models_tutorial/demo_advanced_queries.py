#!/usr/bin/env python
"""
Advanced Django Queries Tutorial Demo

This script demonstrates advanced query concepts from:
https://docs.djangoproject.com/en/5.2/topics/db/queries/

Using the original tutorial models and our existing models.
"""

import os
import sys
import django
from datetime import date, datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db.models import Q, F, Count, Avg, Max, Min, Sum, Case, When, Value
from django.db.models.functions import Upper, Lower, Length, Concat
from django.db import connection, models
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

# Import models from our existing blog app
from blog.models import (
    Person, PersonExtended, Musician, Album, Topping, Pizza,
    Group, Membership, Place, Restaurant, Student, Runner, Ox,
    StudentChild, Blog as BlogModel
)

def create_sample_data():
    """Create comprehensive sample data for query demonstrations"""
    print("=" * 60)
    print("CREATING SAMPLE DATA")
    print("=" * 60)
    
    # Create blogs
    blogs_data = [
        ("Beatles Blog", "All the latest Beatles news"),
        ("Python Programming", "Advanced Python techniques and tutorials"),
        ("Django Tips", "Best practices for Django development"),
        ("Web Development", "Modern web development trends"),
        ("Music Reviews", "In-depth album and concert reviews"),
    ]
    
    blogs = []
    for name, tagline in blogs_data:
        blog, created = BlogModel.objects.get_or_create(
            name=name,
            defaults={'tagline': tagline}
        )
        blogs.append(blog)
        if created:
            print(f"Created blog: {name}")
    
    # Create musicians with more variety
    musicians_data = [
        ("John", "Lennon", "Guitar", "Rock"),
        ("Paul", "McCartney", "Bass", "Rock"),
        ("George", "Harrison", "Guitar", "Rock"),
        ("Ringo", "Starr", "Drums", "Rock"),
        ("Miles", "Davis", "Trumpet", "Jazz"),
        ("Charlie", "Parker", "Saxophone", "Jazz"),
        ("Bob", "Dylan", "Guitar", "Folk"),
        ("Joni", "Mitchell", "Guitar", "Folk"),
    ]
    
    musicians = []
    for first, last, instrument, genre in musicians_data:
        musician, created = Musician.objects.get_or_create(
            first_name=first,
            last_name=last,
            defaults={'instrument': instrument}
        )
        musicians.append(musician)
        if created:
            print(f"Created musician: {first} {last}")
    
    # Create albums with varied data
    albums_data = [
        ("Abbey Road", musicians[0], date(1969, 9, 26), 5, 15, 3),
        ("Sgt. Pepper's", musicians[1], date(1967, 6, 1), 5, 20, 2),
        ("Revolver", musicians[2], date(1966, 8, 5), 4, 12, 1),
        ("Help!", musicians[3], date(1965, 8, 6), 4, 8, 0),
        ("Kind of Blue", musicians[4], date(1959, 8, 17), 5, 25, 1),
        ("Bird and Diz", musicians[5], date(1952, 6, 1), 4, 5, 0),
        ("Highway 61 Revisited", musicians[6], date(1965, 8, 30), 5, 18, 2),
        ("Blue", musicians[7], date(1971, 6, 22), 5, 22, 1),
    ]
    
    albums = []
    for name, artist, release_date, stars, comments, pingbacks in albums_data:
        album, created = Album.objects.get_or_create(
            name=name,
            artist=artist,
            defaults={
                'release_date': release_date,
                'num_stars': stars,
                # Adding number_of_comments and number_of_pingbacks if the model has them
            }
        )
        albums.append(album)
        if created:
            print(f"Created album: {name} by {artist}")
    
    # Create students with more data
    students_data = [
        ("Alice", "Johnson", "alice@university.edu", "SO", 2026),
        ("Bob", "Smith", "bob@university.edu", "JR", 2025),
        ("Carol", "Davis", "carol@university.edu", "SR", 2024),
        ("David", "Wilson", "david@university.edu", "FR", 2027),
        ("Eve", "Brown", "eve@university.edu", "GR", 2024),
        ("Frank", "Miller", "frank@university.edu", "SO", 2026),
        ("Grace", "Taylor", "grace@university.edu", "JR", 2025),
    ]
    
    students = []
    for first, last, email, year, grad_year in students_data:
        student, created = Student.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first,
                'last_name': last,
                'year_in_school': year,
                'graduation_year': grad_year
            }
        )
        students.append(student)
        if created:
            print(f"Created student: {first} {last}")
    
    print(f"\nSample data creation completed!")
    return blogs, musicians, albums, students

def demo_advanced_filtering():
    print("\n" + "=" * 60)
    print("ADVANCED FILTERING TECHNIQUES")
    print("=" * 60)
    
    # Range queries
    print("1. Range queries:")
    recent_albums = Album.objects.filter(release_date__range=(date(1965, 1, 1), date(1970, 12, 31)))
    print(f"Albums from 1965-1970: {[f'{a.name} ({a.release_date.year})' for a in recent_albums]}")
    
    # Year, month, day extraction
    print("\n2. Date field extraction:")
    albums_1969 = Album.objects.filter(release_date__year=1969)
    print(f"Albums from 1969: {[a.name for a in albums_1969]}")
    
    summer_albums = Album.objects.filter(release_date__month__in=[6, 7, 8])
    # print(f"Summer albums (Jun-Aug): {[f'{a.name} ({a.release_date.strftime(\"%b %Y\")})' for a in summer_albums]}")
    
    # In queries
    print("\n3. IN queries:")
    top_musicians = Musician.objects.filter(last_name__in=['Lennon', 'McCartney', 'Davis'])
    print(f"Top musicians: {[str(m) for m in top_musicians]}")
    
    # Greater than, less than
    print("\n4. Comparison queries:")
    high_rated = Album.objects.filter(num_stars__gte=5)
    print(f"5-star albums: {[a.name for a in high_rated]}")
    
    # Null checks
    print("\n5. Null checks:")
    students_with_grad_year = Student.objects.filter(graduation_year__isnull=False)
    print(f"Students with graduation year: {len(students_with_grad_year)}")

def demo_complex_q_queries():
    print("\n" + "=" * 60)
    print("COMPLEX Q OBJECT QUERIES")
    print("=" * 60)
    
    # Complex OR conditions
    print("1. Complex OR conditions:")
    rock_or_jazz = Musician.objects.filter(
        Q(instrument="Guitar") | Q(instrument="Trumpet") | Q(instrument="Saxophone")
    )
    print(f"Guitar/Trumpet/Sax players: {[str(m) for m in rock_or_jazz]}")
    
    # Combining AND and OR
    print("\n2. Combining AND and OR:")
    complex_query = Album.objects.filter(
        (Q(num_stars=5) | Q(num_stars=4)) & 
        Q(release_date__year__gte=1965)
    )
    print(f"High-rated albums from 1965+: {[f'{a.name} ({a.num_stars} stars)' for a in complex_query]}")
    
    # Negation with Q objects
    print("\n3. Negation with Q objects:")
    not_guitar = Musician.objects.filter(~Q(instrument="Guitar"))
    print(f"Non-guitarists: {[f'{m} ({m.instrument})' for m in not_guitar]}")
    
    # Dynamic Q object construction
    print("\n4. Dynamic Q object construction:")
    search_terms = ["Beatles", "Python", "Django"]
    q_objects = Q()
    for term in search_terms:
        q_objects |= Q(name__icontains=term)
    
    matching_blogs = BlogModel.objects.filter(q_objects)
    print(f"Blogs matching search terms: {[b.name for b in matching_blogs]}")

def demo_f_expressions_advanced():
    print("\n" + "=" * 60)
    print("ADVANCED F EXPRESSIONS")
    print("=" * 60)
    
    # Create some test data with comments and pingbacks
    print("1. Comparing fields with F expressions:")
    # For demonstration, let's filter albums by name length
    long_named_albums = Album.objects.annotate(
        name_length=Length('name')
    ).filter(name_length__gt=10)
    print(f"Albums with long names: {[f'{a.name} (length: {Length(a.name)})' for a in long_named_albums]}")
    
    # Mathematical operations with F expressions
    print("\n2. Mathematical operations:")
    # Since our Album model might not have comments/pingbacks, let's use existing fields
    albums_with_calc = Album.objects.annotate(
        rating_doubled=F('num_stars') * 2,
        rating_plus_year=F('num_stars') + F('release_date__year') - 1900
    )
    
    for album in albums_with_calc[:3]:
        print(f"{album.name}: rating*2={album.rating_doubled}, rating+year-1900={album.rating_plus_year}")
    
    # String operations
    print("\n3. String operations with F expressions:")
    musicians_with_full_name = Musician.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )
    
    for musician in musicians_with_full_name[:3]:
        print(f"Full name: {musician.full_name}")

def demo_aggregation_advanced():
    print("\n" + "=" * 60)
    print("ADVANCED AGGREGATION")
    print("=" * 60)
    
    # Basic aggregation across all records
    print("1. Basic aggregation:")
    album_stats = Album.objects.aggregate(
        total=Count('id'),
        avg_rating=Avg('num_stars'),
        max_rating=Max('num_stars'),
        min_rating=Min('num_stars'),
        total_stars=Sum('num_stars')
    )
    print(f"Album statistics: {album_stats}")
    
    # Grouping with annotations
    print("\n2. Grouping with annotations:")
    musician_stats = Musician.objects.annotate(
        album_count=Count('album'),
        avg_rating=Avg('album__num_stars'),
        best_album_rating=Max('album__num_stars')
    ).filter(album_count__gt=0)
    
    print("Musician statistics:")
    for musician in musician_stats:
        print(f"  {musician}: {musician.album_count} albums, "
              f"avg: {musician.avg_rating:.1f}, best: {musician.best_album_rating}")
    
    # Conditional aggregation
    print("\n3. Conditional aggregation:")
    student_stats = Student.objects.aggregate(
        total_students=Count('id'),
        undergrad_count=Count(Case(
            When(year_in_school__in=['FR', 'SO', 'JR', 'SR'], then=1)
        )),
        grad_count=Count(Case(
            When(year_in_school='GR', then=1)
        ))
    )
    print(f"Student statistics: {student_stats}")

def demo_subqueries():
    print("\n" + "=" * 60)
    print("SUBQUERIES AND EXISTS")
    print("=" * 60)
    
    # Subquery with IN
    print("1. Subquery with IN:")
    top_rated_album_ids = Album.objects.filter(num_stars=5).values_list('id', flat=True)
    musicians_with_top_albums = Musician.objects.filter(album__id__in=top_rated_album_ids).distinct()
    print(f"Musicians with 5-star albums: {[str(m) for m in musicians_with_top_albums]}")
    
    # EXISTS equivalent
    print("\n2. EXISTS queries:")
    musicians_with_albums = Musician.objects.filter(album__isnull=False).distinct()
    print(f"Musicians with albums: {[str(m) for m in musicians_with_albums]}")
    
    musicians_without_albums = Musician.objects.filter(album__isnull=True)
    print(f"Musicians without albums: {[str(m) for m in musicians_without_albums]}")

def demo_advanced_ordering():
    print("\n" + "=" * 60)
    print("ADVANCED ORDERING")
    print("=" * 60)
    
    # Multiple field ordering
    print("1. Multiple field ordering:")
    albums_ordered = Album.objects.order_by('-num_stars', 'release_date', 'name')
    print("Albums ordered by rating (desc), then date, then name:")
    for album in albums_ordered:
        print(f"  {album.name} ({album.num_stars} stars, {album.release_date.year})")
    
    # Ordering by related fields
    print("\n2. Ordering by related fields:")
    albums_by_artist_name = Album.objects.order_by('artist__last_name', 'artist__first_name')
    print("Albums ordered by artist name:")
    for album in albums_by_artist_name:
        print(f"  {album.name} by {album.artist}")
    
    # Case-insensitive ordering
    print("\n3. Case-insensitive ordering:")
    blogs_case_insensitive = BlogModel.objects.annotate(
        name_lower=Lower('name')
    ).order_by('name_lower')
    print("Blogs ordered case-insensitively:")
    for blog in blogs_case_insensitive:
        print(f"  {blog.name}")

def demo_select_related_prefetch():
    print("\n" + "=" * 60)
    print("SELECT_RELATED & PREFETCH_RELATED OPTIMIZATION")
    print("=" * 60)
    
    # Without optimization - multiple queries
    print("1. Without optimization (multiple DB queries):")
    print("Querying albums and their artists...")
    albums = Album.objects.all()
    for album in albums[:3]:
        print(f"  {album.name} by {album.artist.first_name} {album.artist.last_name}")
    
    # With select_related - single query with JOIN
    print("\n2. With select_related (single query with JOIN):")
    print("Querying albums with artists in one query...")
    albums_optimized = Album.objects.select_related('artist').all()
    for album in albums_optimized[:3]:
        print(f"  {album.name} by {album.artist.first_name} {album.artist.last_name}")
    
    # Show the SQL being generated
    print("\n3. SQL Query for select_related:")
    query = Album.objects.select_related('artist').all()[:3]
    print(f"SQL: {query.query}")

def demo_annotations_case_when():
    print("\n" + "=" * 60)
    print("ANNOTATIONS WITH CASE/WHEN")
    print("=" * 60)
    
    # Conditional annotations
    print("1. Conditional annotations:")
    albums_with_rating_category = Album.objects.annotate(
        rating_category=Case(
            When(num_stars=5, then=Value('Excellent')),
            When(num_stars=4, then=Value('Good')),
            When(num_stars=3, then=Value('Average')),
            default=Value('Poor'),
            output_field=models.CharField()
        )
    )
    
    for album in albums_with_rating_category:
        print(f"  {album.name}: {album.rating_category} ({album.num_stars} stars)")
    
    # Counting with conditions
    print("\n2. Counting with conditions:")
    musician_album_breakdown = Musician.objects.annotate(
        total_albums=Count('album'),
        excellent_albums=Count(Case(
            When(album__num_stars=5, then=1)
        )),
        good_albums=Count(Case(
            When(album__num_stars=4, then=1)
        ))
    ).filter(total_albums__gt=0)
    
    for musician in musician_album_breakdown:
        print(f"  {musician}: {musician.total_albums} total, "
              f"{musician.excellent_albums} excellent, {musician.good_albums} good")

def demo_distinct_queries():
    print("\n" + "=" * 60)
    print("DISTINCT QUERIES")
    print("=" * 60)
    
    # Basic distinct
    print("1. Basic distinct:")
    instruments = Musician.objects.values_list('instrument', flat=True).distinct()
    print(f"Distinct instruments: {list(instruments)}")
    
    # Distinct with related fields
    print("\n2. Distinct with related fields:")
    artists_with_albums = Musician.objects.filter(album__isnull=False).distinct()
    print(f"Artists with albums: {[str(a) for a in artists_with_albums]}")
    
    # Distinct on specific fields (PostgreSQL specific)
    print("\n3. Years with album releases:")
    years = Album.objects.values_list('release_date__year', flat=True).distinct().order_by('release_date__year')
    print(f"Years with releases: {list(years)}")

def demo_raw_sql_integration():
    print("\n" + "=" * 60)
    print("RAW SQL INTEGRATION")
    print("=" * 60)
    
    # Using raw SQL
    print("1. Raw SQL queries:")
    raw_musicians = Musician.objects.raw(
        "SELECT * FROM blog_musician WHERE instrument = %s ORDER BY last_name",
        ["Guitar"]
    )
    print("Guitarists (from raw SQL):")
    for musician in raw_musicians:
        print(f"  {musician.first_name} {musician.last_name}")
    
    # Using extra() for custom SQL
    print("\n2. Using extra() for custom SQL:")
    albums_with_decade = Album.objects.extra(
        select={
            'decade': "CAST((strftime('%%Y', release_date) / 10) * 10 AS INTEGER)"
        }
    ).order_by('decade', 'release_date')
    
    print("Albums by decade:")
    current_decade = None
    for album in albums_with_decade:
        if album.decade != current_decade:
            current_decade = album.decade
            print(f"\n  {current_decade}s:")
        print(f"    {album.name} ({album.release_date.year})")
    
    # Direct SQL execution
    print("\n3. Direct SQL execution:")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT b.name as blog_name, COUNT(*) as musician_count
            FROM blog_blogmodel b, blog_musician m 
            WHERE 1=1 
            GROUP BY b.name 
            HAVING COUNT(*) >= 0
            LIMIT 3
        """)
        results = cursor.fetchall()
        print("Custom aggregation results:")
        for blog_name, count in results:
            print(f"  {blog_name}: {count}")

def demo_database_functions():
    print("\n" + "=" * 60)
    print("DATABASE FUNCTIONS")
    print("=" * 60)
    
    # String functions
    print("1. String functions:")
    musicians_upper = Musician.objects.annotate(
        name_upper=Upper('last_name'),
        name_lower=Lower('first_name'),
        name_length=Length('last_name')
    )
    
    for musician in musicians_upper[:3]:
        print(f"  {musician.first_name} {musician.last_name}: "
              f"UPPER={musician.name_upper}, lower={musician.name_lower}, "
              f"length={musician.name_length}")
    
    # Concatenation
    print("\n2. String concatenation:")
    full_names = Musician.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name'),
        full_name_reversed=Concat('last_name', Value(', '), 'first_name')
    )
    
    for musician in full_names[:3]:
        print(f"  Normal: {musician.full_name}")
        print(f"  Reversed: {musician.full_name_reversed}")

def demo_performance_tips():
    print("\n" + "=" * 60)
    print("PERFORMANCE OPTIMIZATION TIPS")
    print("=" * 60)
    
    # Show query count
    print("1. Monitoring query count:")
    from django.db import connection
    
    initial_queries = len(connection.queries)
    
    # Inefficient way
    albums = Album.objects.all()
    for album in albums[:3]:
        print(f"  {album.name} by {album.artist.first_name}")  # N+1 queries
    
    after_inefficient = len(connection.queries)
    
    # Efficient way
    albums_efficient = Album.objects.select_related('artist').all()
    for album in albums_efficient[:3]:
        print(f"  {album.name} by {album.artist.first_name}")  # Single query
    
    after_efficient = len(connection.queries)
    
    print(f"\nQuery count comparison:")
    print(f"  Inefficient approach: {after_inefficient - initial_queries} queries")
    print(f"  Efficient approach: {after_efficient - after_inefficient} queries")
    
    # Only() and defer() for field selection
    print("\n2. Field selection with only() and defer():")
    
    # Only specific fields
    albums_minimal = Album.objects.only('name', 'num_stars')
    print("Albums with only name and rating:")
    for album in albums_minimal[:3]:
        print(f"  {album.name}: {album.num_stars} stars")
    
    # Defer specific fields
    albums_deferred = Album.objects.defer('release_date')
    print("\nAlbums with deferred release_date:")
    for album in albums_deferred[:3]:
        print(f"  {album.name}: {album.num_stars} stars")

def main():
    """Run all advanced query demonstrations"""
    print("Advanced Django Queries Tutorial")
    print("=" * 60)
    
    # Create sample data
    blogs, musicians, albums, students = create_sample_data()
    
    # Run all demonstrations
    demo_advanced_filtering()
    demo_complex_q_queries()
    demo_f_expressions_advanced()
    demo_aggregation_advanced()
    demo_subqueries()
    demo_advanced_ordering()
    demo_select_related_prefetch()
    demo_annotations_case_when()
    demo_distinct_queries()
    demo_raw_sql_integration()
    demo_database_functions()
    demo_performance_tips()
    
    print(f"\n🚀 Advanced queries tutorial completed!")
    print(f"📊 Key advanced concepts covered:")
    print(f"  • Complex filtering and Q objects")
    print(f"  • F expressions for field comparisons")
    print(f"  • Advanced aggregation and annotations")
    print(f"  • Subqueries and EXISTS queries")
    print(f"  • Query optimization techniques")
    print(f"  • Database functions and raw SQL")
    print(f"  • Performance monitoring and tips")

if __name__ == "__main__":
    main()
