from django.contrib import admin
from .models import Project, BlogPost, Contact, Testimonial

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'client', 'location', 'created_at')
    list_filter = ('category', 'date')
    search_fields = ('title', 'category', 'client', 'location')
    date_hierarchy = 'date'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'comments_count', 'created_at')
    list_filter = ('date', 'author')
    search_fields = ('title', 'author')
    date_hierarchy = 'date'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    date_hierarchy = 'created_at'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'created_at')
    search_fields = ('name', 'position')
    date_hierarchy = 'created_at'