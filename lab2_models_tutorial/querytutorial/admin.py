from django.contrib import admin
from .models import Blog, Author, Entry, Dog, Category, Tag, ExtendedEntry, Comment

# Register the models from the Django queries tutorial
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline')
    search_fields = ('name', 'tagline')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'blog', 'pub_date', 'rating', 'number_of_comments')
    list_filter = ('blog', 'pub_date', 'rating')
    search_fields = ('headline', 'body_text')
    filter_horizontal = ('authors',)
    date_hierarchy = 'pub_date'

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'data')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

@admin.register(ExtendedEntry)
class ExtendedEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog', 'pub_date', 'is_published', 'featured', 'view_count')
    list_filter = ('is_published', 'featured', 'pub_date', 'categories', 'tags')
    search_fields = ('title', 'content')
    filter_horizontal = ('authors', 'categories', 'tags')
    date_hierarchy = 'pub_date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'entry', 'created_date', 'is_approved', 'rating')
    list_filter = ('is_approved', 'rating', 'created_date')
    search_fields = ('author_name', 'content')
    date_hierarchy = 'created_date'
