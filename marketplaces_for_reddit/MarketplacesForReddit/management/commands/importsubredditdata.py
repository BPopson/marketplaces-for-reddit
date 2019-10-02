from datetime import datetime
from pprint import pprint

import praw

from django.core.management.base import BaseCommand
from MarketplacesForReddit.models import Listing, ParsedListing


class Command(BaseCommand):
    help = 'Import data from a particular subreddit'

    def add_arguments(self, parser):
        parser.add_argument('--reddit_api_personal_use_script',
                            nargs=1,
                            help='The 14-character personal use script key from the Reddit API registration page',
                            type=str,
                            required=True)
        parser.add_argument('--reddit_api_secret',
                            nargs=1,
                            help='The 27-character secret key from the Reddit API registration page',
                            type=str,
                            required=True)
        parser.add_argument('--subreddit',
                            nargs=1,
                            help='The subreddit to obtain data from (e.g. hardwareswap)',
                            type=str,
                            required=True)
        parser.add_argument('--sort_by',
                            choices=['hot', 'new', 'controversial', 'top', 'rising'],
                            help='The method to sort the subreddit data by (default: top)')
        parser.add_argument('--limit',
                            nargs=1,
                            type=int,
                            help='How many listings to be returned from the specified subreddit (default: 25)')

    def handle(self, *args, **options):
        option_client_id = options['reddit_api_personal_use_script'][0]
        option_client_secret = options['reddit_api_secret'][0]
        option_subreddit = options['subreddit'][0]
        option_limit = options['limit'][0]
        option_sort_by = options['sort_by']

        reddit = praw.Reddit(client_id=option_client_id,
                             client_secret=option_client_secret,
                             user_agent='windows:PRAW_testing:v0.0.2 (by /u/Doritos_man)')
        subreddit = reddit.subreddit(option_subreddit)

        limit = option_limit if option_limit is not None else 25

        if option_sort_by == 'hot':
            submissions = subreddit.hot(limit=limit)
        elif option_sort_by == 'new':
            submissions = subreddit.new(limit=limit)
        elif option_sort_by == 'controversial':
            submissions = subreddit.controversial(limit=limit)
        elif option_sort_by == 'top':
            submissions = subreddit.top(limit=limit)
        elif option_sort_by == 'rising':
            submissions = subreddit.rising(limit=limit)
        else:
            submissions = subreddit.top(limit=limit)

        for submission in submissions:
            pprint(vars(submission))
            listing = Listing()
            parsed_listing = ParsedListing()
            listing.id = submission.id
            listing.author = submission.author.name
            listing.author_flair_text = submission.author_flair_text
            listing.author_fullname = submission.author_fullname
            listing.created_utc = get_date(submission.created_utc)
            listing.domain = submission.domain
            listing.edited = get_date(submission.edited)
            listing.link_flair_css_class = submission.link_flair_css_class
            listing.link_flair_text = submission.link_flair_text
            listing.name = submission.name
            listing.permalink = submission.permalink
            listing.selftext = submission.selftext
            listing.selftext_html = submission.selftext_html
            listing.subreddit = submission.subreddit.display_name
            listing.subreddit_id = submission.subreddit_id
            listing.subreddit_name_prefixed = submission.subreddit_name_prefixed
            listing.title = submission.title
            listing.url = submission.url
            parsed_listing.id = listing
            if (len(listing.get_location()) > 10):
                parsed_listing.location = 'Invalid'
            else:
                parsed_listing.location = listing.get_location()
            parsed_listing.has = listing.get_has()
            parsed_listing.wants = listing.get_wants()
            pprint(vars(listing))
            listing.save()
            parsed_listing.save()


def get_date(created):
    return datetime.fromtimestamp(created)

