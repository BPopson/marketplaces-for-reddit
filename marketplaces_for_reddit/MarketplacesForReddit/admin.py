from django.contrib import admin

from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_utc', 'link_flair_text', 'subreddit_name_prefixed', 'get_wants', 'get_has', 'get_location')
    list_filter = ['link_flair_text', 'created_utc']
    search_fields = ['title']


# Register your models here.
admin.site.register(Listing, ListingAdmin)
