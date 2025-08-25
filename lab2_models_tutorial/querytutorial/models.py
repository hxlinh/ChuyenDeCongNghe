from datetime import date
from django.db import models

# These are the exact models from the Django queries tutorial
# https://docs.djangoproject.com/en/5.2/topics/db/queries/

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline

# Additional model for JSONField demonstrations
class Dog(models.Model):
    name = models.CharField(max_length=200)
    data = models.JSONField(null=True)

    def __str__(self):
        return self.name

# Model for advanced relationship demonstrations
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#000000")  # Hex color

    def __str__(self):
        return self.name

# Extended Entry model with more relationships
class ExtendedEntry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(Author, related_name='extended_entries')
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "extended entries"

# Model for demonstrating complex queries
class Comment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)

    def __str__(self):
        return f"Comment by {self.author_name} on {self.entry.headline}"

    class Meta:
        ordering = ['-created_date']
