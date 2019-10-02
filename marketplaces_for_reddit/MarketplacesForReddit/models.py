import string

from django.contrib.postgres.fields import JSONField
from django.db import models


# Create your models here.
class Listing(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    author = models.CharField(max_length=20)
    author_flair_text = models.CharField(max_length=50, null=True)
    author_fullname = models.CharField(max_length=16)
    created_utc = models.DateTimeField()
    domain = models.CharField(max_length=25)
    edited = models.DateTimeField()
    link_flair_css_class = models.CharField(max_length=50, null=True)
    link_flair_text = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50)
    permalink = models.CharField(max_length=300)
    selftext = models.TextField(null=True)
    selftext_html = models.TextField(null=True)
    subreddit = models.CharField(max_length=20)
    subreddit_id = models.CharField(max_length=8)
    subreddit_name_prefixed = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=300)

    def get_wants(self):
        title = self.title.upper()
        have_location = title.find('[H]')
        want_location = title.find('[W]')

        if have_location == -1 or want_location == -1:
            return 'N/A'
        elif have_location > want_location:
            return self.title[want_location:have_location]
        else:
            return self.title[want_location:]

    def get_has(self):
        title = self.title.upper()
        have_location = title.find('[H]')
        want_location = title.find('[W]')

        if have_location == -1 or want_location == -1:
            return 'N/A'
        elif have_location > want_location:
            return self.title[have_location:]
        else:
            return self.title[have_location:want_location]

    def get_location(self):
        title = self.title.upper()
        location_start = title.find('[')
        location_end = title.find(']')

        if location_start == -1 or location_end == -1:
            return 'N/A'
        else:
            return self.title[location_start:location_end+1]

    def get_number_of_trades(self):
        if self.author_flair_text is None:
            return 0

        trades_text = self.author_flair_text.upper()
        trades_text_location = trades_text.find('TRADES:')

        if trades_text_location == -1:
            return 'N/A: Invalid Flair Text'
        else:
            return self.author_flair_text[7:]

class ParsedListing(models.Model):
    id = models.OneToOneField(Listing, primary_key=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=10)
    has = models.CharField(max_length=300)
    wants = models.CharField(max_length=300)