"""
Django Initial Data Tutorial - Interactive Shell Demo

Run this script in the Django shell to explore initial data:
python manage.py shell < initial_data_shell_demo.py

Or copy and paste sections into the Django shell.
"""

print("="*60)
print("  Django Initial Data Tutorial - Interactive Demo")
print("="*60)

# Import models
from library.models import Author, Category, Book, Review
from django.core.management import call_command
import json
from datetime import date

print("\n--- 1. Current Data State ---")
print(f"Authors: {Author.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Books: {Book.objects.count()}")
print(f"Reviews: {Review.objects.count()}")

if Author.objects.exists():
    print("\nSample Authors:")
    for author in Author.objects.all()[:3]:
        print(f"  - {author.name} ({author.email})")

if Book.objects.exists():
    print("\nSample Books:")
    for book in Book.objects.all()[:3]:
        print(f"  - {book.title} by {book.author.name}")

print("\n--- 2. Loading Fixtures Programmatically ---")

# You can load fixtures programmatically using call_command
print("Loading authors fixture...")
try:
    call_command('loaddata', 'initial_authors', verbosity=1)
    print(f"✅ Authors loaded. Total: {Author.objects.count()}")
except Exception as e:
    print(f"❌ Error loading authors: {e}")

print("Loading categories fixture...")
try:
    call_command('loaddata', 'initial_categories', verbosity=1)
    print(f"✅ Categories loaded. Total: {Category.objects.count()}")
except Exception as e:
    print(f"❌ Error loading categories: {e}")

print("\n--- 3. Creating Data Programmatically ---")

# Example of creating data in shell (similar to data migration)
print("Creating additional author...")
author_data = {
    'name': 'Neil Gaiman',
    'email': 'neil.gaiman@example.com',
    'birth_date': date(1960, 11, 10),
    'bio': 'English author of short fiction, novels, comic books, graphic novels, and films.'
}

author, created = Author.objects.get_or_create(
    name=author_data['name'],
    defaults=author_data
)

if created:
    print(f"✅ Created new author: {author.name}")
else:
    print(f"ℹ️  Author already exists: {author.name}")

print("\n--- 4. Exploring Relationships ---")

if Book.objects.exists():
    print("Books with their authors and categories:")
    for book in Book.objects.select_related('author', 'category').all()[:5]:
        category_name = book.category.name if book.category else "No category"
        print(f"  📖 {book.title}")
        print(f"     Author: {book.author.name}")
        print(f"     Category: {category_name}")
        print(f"     Published: {book.publication_date}")
        print(f"     Price: ${book.price}")
        print()

print("\n--- 5. Query Examples ---")

# Find books by specific author
jk_books = Book.objects.filter(author__name__icontains='rowling')
print(f"Books by J.K. Rowling: {jk_books.count()}")
for book in jk_books:
    print(f"  - {book.title} ({book.publication_date.year})")

# Find books in specific category
fantasy_books = Book.objects.filter(category__name='Fantasy')
print(f"\nFantasy books: {fantasy_books.count()}")
for book in fantasy_books:
    print(f"  - {book.title}")

# Find books with reviews
books_with_reviews = Book.objects.filter(reviews__isnull=False).distinct()
print(f"\nBooks with reviews: {books_with_reviews.count()}")
for book in books_with_reviews[:3]:
    avg_rating = book.reviews.aggregate(avg=models.Avg('rating'))['avg']
    print(f"  - {book.title} (Avg rating: {avg_rating:.1f})")

print("\n--- 6. Data Export Example ---")

# Export data (similar to dumpdata)
print("Sample data export (first 2 authors):")
authors_data = []
for author in Author.objects.all()[:2]:
    authors_data.append({
        'model': 'library.author',
        'pk': author.pk,
        'fields': {
            'name': author.name,
            'email': author.email,
            'birth_date': author.birth_date.isoformat() if author.birth_date else None,
            'bio': author.bio,
        }
    })

print(json.dumps(authors_data, indent=2))

print("\n--- 7. Useful Commands for Continued Exploration ---")

commands = [
    "# List all authors",
    "Author.objects.all()",
    "",
    "# Find specific author",
    "Author.objects.get(name='J.K. Rowling')",
    "",
    "# Books published after 1980",
    "Book.objects.filter(publication_date__year__gt=1980)",
    "",
    "# Most expensive books",
    "Book.objects.order_by('-price')[:5]",
    "",
    "# Authors with most books",
    "from django.db.models import Count",
    "Author.objects.annotate(book_count=Count('books')).order_by('-book_count')",
    "",
    "# Load more fixtures",
    "call_command('loaddata', 'initial_books')",
    "call_command('loaddata', 'initial_reviews')",
    "",
    "# Create new records",
    "new_author = Author.objects.create(",
    "    name='Your Name',",
    "    email='your@email.com'",
    ")",
]

print("\n💡 Try these commands in the Django shell:")
for cmd in commands:
    print(f"   {cmd}")

print("\n" + "="*60)
print("  Interactive Demo Complete!")
print("  Continue exploring in the Django shell...")
print("="*60)
