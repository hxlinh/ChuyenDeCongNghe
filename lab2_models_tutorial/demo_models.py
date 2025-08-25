#!/usr/bin/env python
"""
Django Models Tutorial Demo Script

This script demonstrates all the concepts from the Django models tutorial:
https://docs.djangoproject.com/en/5.2/topics/db/models/
"""

import os
import sys
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.models import (
    Person, PersonExtended, Musician, Album, Topping, Pizza,
    Group, Membership, Place, Restaurant, Student, Runner, Ox,
    StudentChild, Blog
)

def demo_basic_models():
    print("=" * 50)
    print("1. BASIC MODELS DEMO")
    print("=" * 50)
    
    # Create some basic Person instances
    person1 = Person.objects.create(first_name="John", last_name="Doe")
    person2 = Person.objects.create(first_name="Jane", last_name="Smith")
    
    print(f"Created persons:")
    for person in Person.objects.all():
        print(f"  - {person}")
    
    print(f"\nTotal persons: {Person.objects.count()}")

def demo_field_types_and_options():
    print("\n" + "=" * 50)
    print("2. FIELD TYPES AND OPTIONS DEMO")
    print("=" * 50)
    
    # Create students with choices field (use get_or_create to avoid duplicates)
    student1, created = Student.objects.get_or_create(
        email="alice@university.edu",
        defaults={
            'first_name': "Alice",
            'last_name': "Johnson",
            'year_in_school': "SO",
            'graduation_year': 2026,
        }
    )
    
    student2, created = Student.objects.get_or_create(
        email="bob@university.edu",
        defaults={
            'first_name': "Bob",
            'last_name': "Wilson",
            'year_in_school': "GR",
        }
    )
    
    print("Created students:")
    for student in Student.objects.all():
        print(f"  - {student}")
        print(f"    Email: {student.email}")
        if student.graduation_year:
            print(f"    Graduation Year: {student.graduation_year}")
    
    # Demo choices with TextChoices (use get_or_create to avoid duplicates)
    runner1, created = Runner.objects.get_or_create(
        name="Usain Bolt",
        defaults={'medal': "GOLD"}
    )
    runner2, created = Runner.objects.get_or_create(
        name="John Runner",
        defaults={'medal': ''}  # No medal
    )
    
    print(f"\nRunners:")
    for runner in Runner.objects.all():
        print(f"  - {runner}")

def demo_relationships():
    print("\n" + "=" * 50)
    print("3. RELATIONSHIPS DEMO")
    print("=" * 50)
    
    # Many-to-one (ForeignKey) relationship
    print("Many-to-one (Musician -> Albums):")
    musician1, created = Musician.objects.get_or_create(
        first_name="Paul", 
        last_name="McCartney",
        defaults={'instrument': "Bass"}
    )
    musician2, created = Musician.objects.get_or_create(
        first_name="John", 
        last_name="Lennon",
        defaults={'instrument': "Guitar"}
    )
    
    album1, created = Album.objects.get_or_create(
        name="Band on the Run",
        defaults={
            'artist': musician1,
            'release_date': date(1973, 12, 5),
            'num_stars': 5
        }
    )
    album2, created = Album.objects.get_or_create(
        name="Ram",
        defaults={
            'artist': musician1,
            'release_date': date(1971, 5, 17),
            'num_stars': 4
        }
    )
    
    print(f"  Musician: {musician1}")
    print(f"  Albums by {musician1}:")
    for album in musician1.album_set.all():
        print(f"    - {album} ({album.release_date}, {album.num_stars} stars)")
    
    # Many-to-many relationship
    print(f"\nMany-to-many (Pizza -> Toppings):")
    pepperoni, created = Topping.objects.get_or_create(name="Pepperoni")
    cheese, created = Topping.objects.get_or_create(name="Cheese")
    mushrooms, created = Topping.objects.get_or_create(name="Mushrooms")
    
    pizza1, created = Pizza.objects.get_or_create(name="Margherita")
    if created:
        pizza1.toppings.add(cheese)
    
    pizza2, created = Pizza.objects.get_or_create(name="Pepperoni Special")
    if created:
        pizza2.toppings.add(pepperoni, cheese)
    
    pizza3, created = Pizza.objects.get_or_create(name="Veggie Supreme")
    if created:
        pizza3.toppings.add(cheese, mushrooms)
    
    for pizza in Pizza.objects.all():
        toppings_list = ", ".join([t.name for t in pizza.toppings.all()])
        print(f"  - {pizza}: {toppings_list}")

def demo_many_to_many_through():
    print("\n" + "=" * 50)
    print("4. MANY-TO-MANY WITH THROUGH MODEL DEMO")
    print("=" * 50)
    
    # Get existing persons or create new ones
    try:
        ringo = Person.objects.get(first_name="Ringo")
    except Person.DoesNotExist:
        ringo = Person.objects.create(first_name="Ringo", last_name="Starr")
    
    try:
        paul = Person.objects.get(first_name="Paul")
    except Person.DoesNotExist:
        paul = Person.objects.create(first_name="Paul", last_name="McCartney")
    
    # Create a group
    beatles = Group.objects.create(name="The Beatles")
    
    # Create memberships with additional information
    m1 = Membership.objects.create(
        person=ringo,
        group=beatles,
        date_joined=date(1962, 8, 16),
        invite_reason="Needed a new drummer."
    )
    
    m2 = Membership.objects.create(
        person=paul,
        group=beatles,
        date_joined=date(1960, 8, 1),
        invite_reason="Wanted to form a band."
    )
    
    print(f"Group: {beatles}")
    print(f"Members:")
    for member in beatles.members.all():
        membership = Membership.objects.get(person=member, group=beatles)
        print(f"  - {member} (joined: {membership.date_joined}, reason: {membership.invite_reason})")
    
    # Query through the relationship
    print(f"\nMembers who joined after 1961:")
    recent_members = beatles.members.filter(membership__date_joined__gt=date(1961, 1, 1))
    for member in recent_members:
        print(f"  - {member}")

def demo_inheritance():
    print("\n" + "=" * 50)
    print("5. MODEL INHERITANCE DEMO")
    print("=" * 50)
    
    # Multi-table inheritance (Restaurant inherits from Place)
    place1 = Place.objects.create(name="Central Park", address="Manhattan, NY")
    restaurant1 = Restaurant.objects.create(
        name="Joe's Pizza",
        address="123 Main St",
        serves_hot_dogs=False,
        serves_pizza=True
    )
    
    print(f"Places:")
    for place in Place.objects.all():
        print(f"  - {place} at {place.address}")
        # Check if it's also a restaurant
        try:
            restaurant = place.restaurant
            print(f"    (Restaurant: Pizza={restaurant.serves_pizza}, Hot Dogs={restaurant.serves_hot_dogs})")
        except Restaurant.DoesNotExist:
            print(f"    (Not a restaurant)")
    
    # Abstract base class inheritance
    student_child = StudentChild.objects.create(
        name="Tommy",
        age=10,
        home_group="A1"
    )
    print(f"\nStudent: {student_child} in group {student_child.home_group}")

def demo_model_methods():
    print("\n" + "=" * 50)
    print("6. MODEL METHODS DEMO")
    print("=" * 50)
    
    # PersonExtended with custom methods
    person_ext = PersonExtended.objects.create(
        first_name="John",
        last_name="Smith",
        birth_date=date(1955, 3, 15)
    )
    
    print(f"Person: {person_ext}")
    print(f"Full name (property): {person_ext.full_name}")
    print(f"Baby boomer status: {person_ext.baby_boomer_status()}")
    
    # Custom save method demo
    print(f"\nTrying to create blogs:")
    blog1 = Blog.objects.create(name="Tech Blog", tagline="All about technology")
    print(f"  Created: {blog1}")
    
    # This won't be saved due to custom save method
    blog2 = Blog(name="Yoko Ono's blog", tagline="Music and art")
    blog2.save()
    print(f"  Attempted to create Yoko's blog...")
    
    print(f"  Total blogs in database: {Blog.objects.count()}")

def demo_meta_options():
    print("\n" + "=" * 50)
    print("7. META OPTIONS DEMO")
    print("=" * 50)
    
    # Create oxen with different horn lengths
    ox1 = Ox.objects.create(horn_length=25)
    ox2 = Ox.objects.create(horn_length=15)
    ox3 = Ox.objects.create(horn_length=30)
    
    print(f"Oxen (ordered by horn length due to Meta.ordering):")
    for ox in Ox.objects.all():
        print(f"  - {ox}")

def clean_up():
    """Optional cleanup function"""
    print("\n" + "=" * 50)
    print("CLEANUP")
    print("=" * 50)
    
    # Count all objects
    models_info = [
        (Person, "Persons"),
        (Student, "Students"),
        (Runner, "Runners"),
        (Musician, "Musicians"),
        (Album, "Albums"),
        (Pizza, "Pizzas"),
        (Topping, "Toppings"),
        (Group, "Groups"),
        (Membership, "Memberships"),
        (Place, "Places"),
        (Restaurant, "Restaurants"),
        (PersonExtended, "Extended Persons"),
        (StudentChild, "Student Children"),
        (Blog, "Blogs"),
        (Ox, "Oxen"),
    ]
    
    print("Current database contents:")
    for model, name in models_info:
        count = model.objects.count()
        if count > 0:
            print(f"  - {name}: {count}")

def main():
    """Run all demos"""
    print("Django Models Tutorial Demonstration")
    print("Based on: https://docs.djangoproject.com/en/5.2/topics/db/models/")
    
    demo_basic_models()
    demo_field_types_and_options()
    demo_relationships()
    demo_many_to_many_through()
    demo_inheritance()
    demo_model_methods()
    demo_meta_options()
    clean_up()
    
    print(f"\n🎉 Tutorial completed! You can now:")
    print(f"  1. Run 'python manage.py runserver' to start the development server")
    print(f"  2. Visit http://127.0.0.1:8000/admin/ to see the admin interface")
    print(f"  3. Login with username 'admin' and the password you set")
    print(f"  4. Explore all the models we created!")

if __name__ == "__main__":
    main()
