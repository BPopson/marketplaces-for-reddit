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
