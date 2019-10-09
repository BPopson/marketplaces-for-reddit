from datetime import date

from django.shortcuts import render

from .models import Listing, ParsedListing
from .forms import SearchForm


# Create your views here.
def index(request):
    context = {}
    listings = Listing.objects.order_by('-created_utc')
    parsed_listings_locations = ParsedListing.objects.values('location').distinct().order_by('location')

    context['listings'] = listings[0:10]
    context['locations'] = parsed_listings_locations

    return render(request, 'home/index.html', context)


def search(request):
    context = {}
    listings = Listing.objects.order_by('-created_utc')
    parsed_listings_locations = ParsedListing.objects.values('location').distinct().order_by('location')

    context['listings'] = listings[0:10]
    context['locations'] = parsed_listings_locations

    context['query_param_location'] = request.GET.get('location', '[USA-TX]')
    context['query_param_date'] = request.GET.get('date', date.today().strftime('%Y-%m-%d'))
    context['query_param_date_within'] = request.GET.get('date_within', '7')
    context['query_param_trade_amount'] = request.GET.get('trade_amount', '1')
    context['query_param_trade_sort'] = request.GET.get('trade_sort', 'gt')
    context['query_param_listing_type'] = request.GET.get('listing_type', 'selling')
    context['query_param_payment_types'] = request.GET.get('payment_types', 'paypal')
    context['search_form'] = SearchForm()

    return render(request, 'search/index.html', context)
