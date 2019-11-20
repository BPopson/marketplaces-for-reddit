from django.contrib import admin

from .models import Listing, ParsedListing, SearchLog


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_utc', 'link_flair_text', 'subreddit_name_prefixed', 'get_wants', 'get_has', 'get_location', 'get_number_of_trades')
    list_filter = ['link_flair_text', 'created_utc']
    search_fields = ['title']

class ParsedListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'has', 'wants')
    list_filter = ['location']

class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'timestamp', 'query_search_text', 'query_location', 'query_date', 'query_date_within', 'query_payment_type', 'query_listing_type')

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(ParsedListing, ParsedListingAdmin)
admin.site.register(SearchLog, SearchLogAdmin)
