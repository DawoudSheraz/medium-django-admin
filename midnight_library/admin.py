"""
Admin for midnight_library app.
"""

from django.contrib import admin
from django.utils.timezone import now, timedelta

from midnight_library.models import (
    Author,
    Book,
    MidnightLibrary,
    Review
)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'is_dead')
    search_fields = ('full_name', 'job', 'user__username')

    def is_dead(self, instance):
        return (instance.date_of_death and instance.date_of_death < now()) or "False"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'library', 'visit_date', 'return_date')
    search_fields = ('title', 'library__author__full_name')

    def return_date(self, instance):
        return instance.visit_date and instance.visit_date + timedelta(days=instance.days_stayed)


@admin.register(MidnightLibrary)
class MidnightLibraryAdmin(admin.ModelAdmin):
    list_display = ('author', 'manager', 'total_lives', 'visited_lives')

    def total_lives(self, instance):
        return instance.collection.count()

    def visited_lives(self, instance):
        return instance.collection.filter(has_visited=True).count()


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('life', 'is_liked')
    search_fields = ('life__library__author__full_name', )
