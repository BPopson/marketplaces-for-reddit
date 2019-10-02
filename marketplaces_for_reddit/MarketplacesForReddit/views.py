from django.shortcuts import render, get_list_or_404

from .models import Listing, ParsedListing
# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-created_utc')
    parsedListings = ParsedListing.objects.values('location').distinct().order_by('location')

    context = {
        'listings': listings[0:10],
        'locations': parsedListings,
    }
    return render(request, 'home/index.html', context)
