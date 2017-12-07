from django.contrib import admin
#import sys
#sys.path.append("..")
from nested_admin.nested import NestedModelAdmin, NestedTabularInline, NestedStackedInline
#from nested_inline.admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline

from .models import Country, Place, Post

class PostInline(NestedStackedInline):
    model = Post
    classes = ['collapse']
    extra = 0

    list_filter = ['pub_date']

class PlaceInline(NestedTabularInline):
    model = Place
    inlines = [PostInline]
    extra = 0

    search_fields = ['place_name']

class CountryAdmin(NestedModelAdmin):
    fieldsets = [
        (None, {'fields': ['country_name']}),
    ]
    inlines = [PlaceInline]

    search_fields = ['country_name']
'''
class PlaceAdmin(NestedModelAdmin):
    fieldsets = [
        (None, {'fields': ['place_name']}),
    ]
    inlines = [PostInline]

    search_fields = ['place_name']
'''
admin.site.register(Country, CountryAdmin)
#admin.site.register(Place, PlaceAdmin)