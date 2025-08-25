"""
Django Queries Tutorial - Interactive Demo

This demonstrates the advanced Django query concepts from:
https://docs.djangoproject.com/en/5.2/topics/db/queries/

Run this in Django shell: python manage.py shell
Then: exec(open('queries_demo_interactive.py').read())
"""

from django.db.models import Q, F, Count, Avg, Max, Min, Sum, Case, When, Value
from django.db.models.functions import Upper, Lower, Length, Concat
from django.db import connection, models
from blog.models import *
from datetime import date, datetime, timedelta
import random

def setup_demo_data():
    """Create rich sample data for query demonstrations"""
    print("Setting up demo data...")
    
    # Clear existing data
    Album.objects.all().delete()
    Musician.objects.all().delete()
    Person.objects.all().delete()
    Student.objects.all().delete()
    
    # Create musicians
    musicians_data = [
        ("John", "Lennon", "Guitar"),
        ("Paul", "McCartney", "Bass"),
        ("George", "Harrison", "Lead Guitar"),
        ("Ringo", "Starr", "Drums"),
        ("Miles", "Davis", "Trumpet"),
        ("Charlie", "Parker", "Saxophone"),
        ("Bob", "Dylan", "Guitar"),
        ("Joni", "Mitchell", "Guitar"),
        ("Stevie", "Wonder", "Piano"),
        ("Ella", "Fitzgerald", "Vocals"),
    ]
    
    musicians = []
    for first, last, instrument in musicians_data:
        musician = Musician.objects.create(
            first_name=first,
            last_name=last,
            instrument=instrument
        )
        musicians.append(musician)
    
    # Create albums with varied ratings and dates
    albums_data = [
        ("Abbey Road", musicians[0], date(1969, 9, 26), 5),
        ("Sgt. Pepper's", musicians[1], date(1967, 6, 1), 5),
        ("Revolver", musicians[2], date(1966, 8, 5), 4),
        ("Help!", musicians[3], date(1965, 8, 6), 4),
        ("Kind of Blue", musicians[4], date(1959, 8, 17), 5),
        ("Bird and Diz", musicians[5], date(1952, 6, 1), 4),
        ("Highway 61 Revisited", musicians[6], date(1965, 8, 30), 5),
        ("Blue", musicians[7], date(1971, 6, 22), 5),
        ("Songs in the Key of Life", musicians[8], date(1976, 9, 28), 5),
        ("Ella Fitzgerald Sings", musicians[9], date(1956, 4, 1), 4),
        ("The White Album", musicians[0], date(1968, 11, 22), 4),
        ("Pet Sounds", musicians[1], date(1966, 5, 16), 5),
    ]
    
    for name, artist, release_date, stars in albums_data:
        Album.objects.create(
            name=name,
            artist=artist,
            release_date=release_date,
            num_stars=stars
        )
    
    # Create students with different graduation years
    students_data = [
        ("Alice", "Johnson", "alice@example.com", "SO", 2026),
        ("Bob", "Smith", "bob@example.com", "JR", 2025),
        ("Carol", "Davis", "carol@example.com", "SR", 2024),
        ("David", "Wilson", "david@example.com", "FR", 2027),
        ("Eve", "Brown", "eve@example.com", "GR", 2024),
        ("Frank", "Miller", "frank@example.com", "SO", 2026),
        ("Grace", "Taylor", "grace@example.com", "JR", 2025),
        ("Henry", "Lee", "henry@example.com", "SR", 2024),
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
    
    print(f"Created {len(musicians)} musicians, {Album.objects.count()} albums, {Student.objects.count()} students")

def demo_basic_queries():
    """Demonstrate basic query operations"""
    print("\n" + "="*60)
    print("BASIC QUERIES")
    print("="*60)
    
    # Simple retrieval
    print("1. Simple object retrieval:")
    try:
        john = Musician.objects.get(first_name="John")
        print(f"   Found: {john}")
    except Musician.DoesNotExist:
        print("   John not found")
    except Musician.MultipleObjectsReturned:
        print("   Multiple Johns found")
    
    # Filtering
    print("\n2. Basic filtering:")
    guitarists = Musician.objects.filter(instrument__icontains="Guitar")
    print(f"   Guitarists: {[str(m) for m in guitarists]}")
    
    # Chaining filters
    print("\n3. Chaining filters:")
    recent_high_rated = Album.objects.filter(
        release_date__year__gte=1965
    ).filter(num_stars__gte=4)
    print(f"   Recent high-rated albums: {[a.name for a in recent_high_rated]}")
    
    # Exclude
    print("\n4. Exclude queries:")
    non_guitarists = Musician.objects.exclude(instrument__icontains="Guitar")
    print(f"   Non-guitarists: {[f'{m} ({m.instrument})' for m in non_guitarists]}")

def demo_field_lookups():
    """Demonstrate field lookup types"""
    print("\n" + "="*60)
    print("FIELD LOOKUPS")
    print("="*60)
    
    # Exact match
    print("1. Exact matches:")
    five_star = Album.objects.filter(num_stars__exact=5)
    print(f"   5-star albums: {[a.name for a in five_star]}")
    
    # Case-insensitive contains
    print("\n2. Case-insensitive contains:")
    beatles_albums = Album.objects.filter(name__icontains="pepper")
    print(f"   Albums with 'pepper': {[a.name for a in beatles_albums]}")
    
    # Starts with / ends with
    print("\n3. Starts with / ends with:")
    albums_starting_with_a = Album.objects.filter(name__istartswith="a")
    albums_ending_with_s = Album.objects.filter(name__endswith="s")
    print(f"   Albums starting with 'A': {[a.name for a in albums_starting_with_a]}")
    print(f"   Albums ending with 's': {[a.name for a in albums_ending_with_s]}")
    
    # Range queries
    print("\n4. Range queries:")
    sixties_albums = Album.objects.filter(
        release_date__range=(date(1960, 1, 1), date(1969, 12, 31))
    )
    print(f"   1960s albums: {[(a.name, a.release_date.year) for a in sixties_albums]}")
    
    # Year/month/day extraction
    print("\n5. Date component extraction:")
    albums_1965 = Album.objects.filter(release_date__year=1965)
    summer_albums = Album.objects.filter(release_date__month__in=[6, 7, 8])
    print(f"   1965 albums: {[a.name for a in albums_1965]}")
    print(f"   Summer albums: {[(a.name, a.release_date.strftime('%b %Y')) for a in summer_albums]}")

def demo_complex_queries():
    """Demonstrate complex Q object queries"""
    print("\n" + "="*60)
    print("COMPLEX Q OBJECT QUERIES")
    print("="*60)
    
    # OR conditions
    print("1. OR conditions with Q objects:")
    guitar_or_piano = Musician.objects.filter(
        Q(instrument__icontains="Guitar") | Q(instrument__icontains="Piano")
    )
    print(f"   Guitar or Piano players: {[f'{m} ({m.instrument})' for m in guitar_or_piano]}")
    
    # AND conditions
    print("\n2. AND conditions:")
    good_recent_albums = Album.objects.filter(
        Q(num_stars__gte=4) & Q(release_date__year__gte=1965)
    )
    print(f"   Good recent albums: {[(a.name, a.num_stars, a.release_date.year) for a in good_recent_albums]}")
    
    # NOT conditions
    print("\n3. NOT conditions:")
    not_five_star = Album.objects.filter(~Q(num_stars=5))
    print(f"   Non-5-star albums: {[(a.name, a.num_stars) for a in not_five_star]}")
    
    # Complex combinations
    print("\n4. Complex combinations:")
    complex_query = Album.objects.filter(
        (Q(num_stars=5) | Q(num_stars=4)) & 
        Q(release_date__year__gte=1965) &
        ~Q(name__icontains="White")
    )
    print(f"   Complex query results: {[(a.name, a.num_stars, a.release_date.year) for a in complex_query]}")

def demo_f_expressions():
    """Demonstrate F expressions for field comparisons"""
    print("\n" + "="*60)
    print("F EXPRESSIONS")
    print("="*60)
    
    # Compare fields (simulation)
    print("1. Mathematical operations with F expressions:")
    albums_with_calculations = Album.objects.annotate(
        rating_doubled=F('num_stars') * 2,
        decade_plus_rating=F('release_date__year') / 10 + F('num_stars')
    )
    
    for album in albums_with_calculations[:5]:
        print(f"   {album.name}: rating*2={album.rating_doubled}, "
              f"decade+rating={album.decade_plus_rating:.1f}")
    
    # String operations
    print("\n2. String operations:")
    musicians_with_full_name = Musician.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name'),
        name_length=Length('last_name')
    )
    
    for musician in musicians_with_full_name[:5]:
        print(f"   {musician.full_name} (last name length: {musician.name_length})")

def demo_aggregation():
    """Demonstrate aggregation functions"""
    print("\n" + "="*60)
    print("AGGREGATION")
    print("="*60)
    
    # Basic aggregation
    print("1. Basic aggregation across all records:")
    album_stats = Album.objects.aggregate(
        total_albums=Count('id'),
        avg_rating=Avg('num_stars'),
        max_rating=Max('num_stars'),
        min_rating=Min('num_stars'),
        total_stars=Sum('num_stars')
    )
    print(f"   Album statistics: {album_stats}")
    
    # Grouping with annotations
    print("\n2. Grouping with annotations:")
    musician_stats = Musician.objects.annotate(
        album_count=Count('album'),
        avg_rating=Avg('album__num_stars'),
        best_rating=Max('album__num_stars')
    ).filter(album_count__gt=0)
    
    print("   Musician statistics:")
    for musician in musician_stats:
        print(f"     {musician}: {musician.album_count} albums, "
              f"avg: {musician.avg_rating:.1f}, best: {musician.best_rating}")
    
    # Conditional aggregation
    print("\n3. Conditional aggregation:")
    student_breakdown = Student.objects.aggregate(
        total_students=Count('id'),
        undergrads=Count(Case(
            When(year_in_school__in=['FR', 'SO', 'JR', 'SR'], then=1)
        )),
        grads=Count(Case(
            When(year_in_school='GR', then=1)
        ))
    )
    print(f"   Student breakdown: {student_breakdown}")

def demo_ordering_and_slicing():
    """Demonstrate ordering and result slicing"""
    print("\n" + "="*60)
    print("ORDERING AND SLICING")
    print("="*60)
    
    # Basic ordering
    print("1. Basic ordering:")
    albums_by_rating = Album.objects.order_by('-num_stars', 'release_date')
    print("   Albums by rating (desc) then date:")
    for album in albums_by_rating[:5]:
        print(f"     {album.name} ({album.num_stars} stars, {album.release_date.year})")
    
    # Ordering by related fields
    print("\n2. Ordering by related fields:")
    albums_by_artist = Album.objects.order_by('artist__last_name', 'artist__first_name')
    print("   Albums by artist name:")
    for album in albums_by_artist[:5]:
        print(f"     {album.name} by {album.artist}")
    
    # Random ordering
    print("\n3. Random ordering:")
    random_albums = Album.objects.order_by('?')[:3]
    print(f"   Random albums: {[a.name for a in random_albums]}")
    
    # Slicing
    print("\n4. Result slicing:")
    top_3_albums = Album.objects.order_by('-num_stars')[:3]
    print(f"   Top 3 albums: {[(a.name, a.num_stars) for a in top_3_albums]}")

def demo_relationships():
    """Demonstrate relationship queries"""
    print("\n" + "="*60)
    print("RELATIONSHIP QUERIES")
    print("="*60)
    
    # Forward relationship
    print("1. Forward relationship (ForeignKey):")
    abbey_road = Album.objects.get(name="Abbey Road")
    print(f"   Album: {abbey_road.name}")
    print(f"   Artist: {abbey_road.artist}")
    print(f"   Artist's instrument: {abbey_road.artist.instrument}")
    
    # Reverse relationship
    print("\n2. Reverse relationship:")
    john = Musician.objects.get(first_name="John")
    john_albums = john.album_set.all()
    print(f"   {john}'s albums: {[a.name for a in john_albums]}")
    
    # Related field filtering
    print("\n3. Filtering by related fields:")
    guitar_albums = Album.objects.filter(artist__instrument__icontains="Guitar")
    print(f"   Albums by guitarists: {[(a.name, a.artist.instrument) for a in guitar_albums]}")
    
    # Spanning relationships
    print("\n4. Spanning multiple relationships:")
    albums_by_johns = Album.objects.filter(artist__first_name="John")
    print(f"   Albums by Johns: {[a.name for a in albums_by_johns]}")

def demo_advanced_features():
    """Demonstrate advanced query features"""
    print("\n" + "="*60)
    print("ADVANCED FEATURES")
    print("="*60)
    
    # Distinct queries
    print("1. Distinct queries:")
    instruments = Musician.objects.values_list('instrument', flat=True).distinct()
    print(f"   Distinct instruments: {list(instruments)}")
    
    # Values and values_list
    print("\n2. Values and values_list:")
    album_data = Album.objects.values('name', 'num_stars', 'artist__first_name')[:3]
    for data in album_data:
        print(f"   {data}")
    
    # Only and defer
    print("\n3. Only and defer for performance:")
    albums_minimal = Album.objects.only('name', 'num_stars')[:3]
    print("   Albums with only name and rating:")
    for album in albums_minimal:
        print(f"     {album.name}: {album.num_stars} stars")
    
    # Raw SQL
    print("\n4. Raw SQL queries:")
    raw_musicians = Musician.objects.raw(
        "SELECT * FROM blog_musician WHERE instrument LIKE %s ORDER BY last_name",
        ["%Guitar%"]
    )
    print("   Guitarists (from raw SQL):")
    for musician in raw_musicians:
        print(f"     {musician.first_name} {musician.last_name}")

def demo_query_optimization():
    """Demonstrate query optimization techniques"""
    print("\n" + "="*60)
    print("QUERY OPTIMIZATION")
    print("="*60)
    
    # Monitor query count
    initial_queries = len(connection.queries)
    
    # Inefficient approach (N+1 queries)
    print("1. Inefficient approach (N+1 problem):")
    albums = Album.objects.all()
    for album in albums[:3]:
        print(f"   {album.name} by {album.artist.first_name}")
    
    after_inefficient = len(connection.queries)
    
    # Efficient approach with select_related
    print("\n2. Efficient approach (select_related):")
    albums_optimized = Album.objects.select_related('artist').all()
    for album in albums_optimized[:3]:
        print(f"   {album.name} by {album.artist.first_name}")
    
    after_efficient = len(connection.queries)
    
    print(f"\n   Query count comparison:")
    print(f"   Inefficient: {after_inefficient - initial_queries} queries")
    print(f"   Efficient: {after_efficient - after_inefficient} queries")
    
    # Show actual SQL
    print("\n3. Generated SQL:")
    query = Album.objects.select_related('artist').all()[:3]
    print(f"   SQL: {query.query}")

def run_complete_demo():
    """Run the complete Django queries demonstration"""
    print("Django Queries Tutorial - Complete Demonstration")
    print("=" * 60)
    print("Based on: https://docs.djangoproject.com/en/5.2/topics/db/queries/")
    print("=" * 60)
    
    # Setup
    setup_demo_data()
    
    # Run all demonstrations
    demo_basic_queries()
    demo_field_lookups()
    demo_complex_queries()
    demo_f_expressions()
    demo_aggregation()
    demo_ordering_and_slicing()
    demo_relationships()
    demo_advanced_features()
    demo_query_optimization()
    
    print(f"\nDjango Queries Tutorial Complete!")
    print(f"Concepts covered:")
    print(f"  • Basic queries and filtering")
    print(f"  • Field lookups and date operations")
    print(f"  • Complex Q object queries")
    print(f"  • F expressions for field operations")
    print(f"  • Aggregation and annotations")
    print(f"  • Ordering and result slicing")
    print(f"  • Relationship traversal")
    print(f"  • Query optimization techniques")
    print(f"  • Raw SQL integration")
    
    print(f"\nNext steps:")
    print(f"  • Explore the Django admin at http://127.0.0.1:8001/admin/")
    print(f"  • Try modifying the queries above")
    print(f"  • Check the Django documentation for more advanced topics")

# Auto-run if executed
if 'run_complete_demo' in locals():
    run_complete_demo()
