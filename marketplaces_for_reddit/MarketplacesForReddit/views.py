from django.shortcuts import render, get_list_or_404

from .models import Listing
# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-created_utc')

    context = {
        'test': "Hello, world. You're at the Marketplaces For Reddit index.",
        'listings': listings[0:15]
    }
    return render(request, 'home/index.html', context)
