from datetime import date, datetime, timedelta

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Listing, ParsedListing
from .forms import SearchForm


# Home Page/Index View
def index(request):
    context = {}
    listings = Listing.objects.order_by('-created_utc')
    parsed_listings_locations = ParsedListing.objects.values('location') \
        .distinct().order_by('location')
    search_form = SearchForm(initial={
        'date': date.today().strftime('%Y-%m-%d'),
        'number_of_trades': 0})

    context['listings'] = listings[0:10]
    context['locations'] = parsed_listings_locations

    context['search_form'] = search_form

    return render(request, 'home/index.html', context)

# Search View
def search(request):
    context = {}

    search_form = SearchForm(request.GET)

    context['query_param_search'] = request.GET.get('search', '')
    context['query_param_search_title_only'] = request.GET.get('search_title_only', False)
    context['query_param_location'] = request.GET.get('location', 'USA')
    context['query_param_date'] = request.GET.get('date', date.today().strftime('%Y-%m-%d'))
    context['query_param_date_within'] = request.GET.get('date_within', '7')
    context['query_param_trade_amount'] = request.GET.get('trade_amount', '1')
    context['query_param_trade_sort'] = request.GET.get('trade_sort', 'gt')
    context['query_param_listing_type'] = request.GET.get('listing_type', 'selling')
    context['query_param_payment_types'] = request.GET.get('payment_types', 'paypal')

    search_params = {
        'search': context['query_param_search'],
        'location': context['query_param_location'],
        'listing_type': context['query_param_listing_type'],
        'payment_types': context['query_param_payment_types'],
        'date': datetime.strptime(context['query_param_date'], '%Y-%m-%d'),
        'date_within': int(context['query_param_date_within']),
    }

    parsed_listings_locations = ParsedListing.objects.values('location') \
        .distinct().order_by('location')
    listings = Listing.objects \
                    .filter(Q(title__icontains=search_params['search']) \
                            | Q(selftext__icontains=search_params['search'])) \
                    .filter(link_flair_text__icontains=search_params['listing_type']) \
                    .filter(title__icontains=search_params['payment_types']) \
                    .filter(created_utc__gte=search_params['date'], \
                            created_utc__lt=search_params['date'].date()
                            + timedelta(days=search_params['date_within'])) \
                    .filter(title__icontains=search_params['location']) \
                    .order_by('-created_utc')

    context['search_form'] = search_form
    context['listings'] = listings[0:25]
    context['locations'] = parsed_listings_locations

    return render(request, 'search/index.html', context)
