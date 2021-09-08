import operator
from datetime import date, timedelta
from functools import reduce

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SearchForm
from .models import Listing, ParsedListing, SearchLog


# Home Page/Index View
def index(request):
    context = {}

    if not request.session.exists(request.session.session_key):
        request.session.create()

    listings = Listing.objects.filter(subreddit__iexact='hardwareswap').order_by('-created_utc')
    # parsed_listings_locations = ParsedListing.objects.values('location') \
    #     .distinct().order_by('location')
    search_form = SearchForm(initial={
        'date': date.today().strftime('%Y-%m-%d'),
        'number_of_trades': 0})

    context['listings'] = listings[0:10]
    # context['locations'] = parsed_listings_locations

    context['search_form'] = search_form

    return render(request, 'home/index.html', context)


# Search View
def search(request):
    context = {}

    if not request.session.exists(request.session.session_key):
        request.session.create()

    search_form = SearchForm(request.GET)
    search_params = {}

    if search_form.is_valid():
        search_params = {
            'search': search_form.cleaned_data['search'],
            'search_title_only': search_form.cleaned_data['search_title_only'],
            'location': search_form.cleaned_data['location'],
            'listing_type': search_form.cleaned_data['listing_type'],
            'payment_type': search_form.cleaned_data['payment_type'],
            'date': search_form.cleaned_data['date'],
            'date_within': int(search_form.cleaned_data['date_within']),
            'number_of_trades': int(search_form.cleaned_data['number_of_trades']),
            'number_of_trades_filter': search_form.cleaned_data['number_of_trades_filter'],
        }

        logged_search = SearchLog()
        logged_search.ip_address = request.META['REMOTE_ADDR']
        logged_search.user_agent = request.META['HTTP_USER_AGENT']
        logged_search.query_string = request.META['QUERY_STRING']
        logged_search.session_id = request.session.session_key
        logged_search.query_search_text = search_params['search']
        logged_search.query_search_title_only = search_params['search_title_only']
        logged_search.query_location = search_params['location']
        logged_search.query_date = search_params['date']
        logged_search.query_date_within = search_params['date_within']
        logged_search.query_trade_amount = search_params['number_of_trades']
        logged_search.query_trade_sort = search_params['number_of_trades_filter']
        logged_search.query_listing_type = search_params['listing_type']
        logged_search.query_payment_type = search_params['payment_type']
        logged_search.save()
    else:
        return HttpResponseRedirect('/')

    # parsed_listings_locations = ParsedListing.objects.values('location') \
    #     .distinct().order_by('location')
    listings = Listing.objects.filter(subreddit__iexact='hardwareswap') \
        .filter(reduce(operator.or_,
                       (Q(link_flair_text__icontains=x) for x in search_params['listing_type']))) \
        .filter(reduce(operator.or_,
                       (Q(title__icontains=x) for x in search_params['payment_type']))) \
        .filter(reduce(operator.or_, (Q(title__icontains=x) for x in search_params['location']))) \
        .filter(created_utc__gte=search_params['date'] - timedelta(days=search_params['date_within']),
                created_utc__lte=search_params['date'] + timedelta(days=search_params['date_within']))

    if search_params['search']:
        if search_params['search_title_only']:
            vector = SearchVector('title')
            query = SearchQuery(search_params['search'])
            # listings = listings.filter(title__icontains=search_params['search'])
            listings = listings.annotate(search=vector).filter(search=query)
        else:
            vector = SearchVector('title', 'selftext')
            query = SearchQuery(search_params['search'])
            listings = listings.annotate(search=vector).filter(search=query)
            # listings = listings.filter(Q(title__icontains=search_params['search']) \
            #                           | Q(selftext__icontains=search_params['search']))

    listings = listings.order_by('-created_utc')

    context['SEARCH_PARAMS'] = search_params
    context['search_form'] = search_form
    context['listings'] = listings[0:25]

    return render(request, 'search/index.html', context)
