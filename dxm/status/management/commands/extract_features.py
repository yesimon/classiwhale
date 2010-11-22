from django.core.management.base import BaseCommand, CommandError
from status.models import *

import extract

class Command(BaseCommand):
    args = '<arg1 arg2 ...>'

    def handle(self, *args, **options):
        tweetId = args[0]
        
        tweet = dict(   id = 12345,
                        text = 'Hi Ken',
                        author = UserProfile.objects.get(id=1), 
                        has_hyperlink = 0, 
                        content_length = 82, 
                        punctuation = 2,
                        hashtags = ['tree', 'frog'],
                        hyperlinks = ['yelp.com', 'yahoo.com', 'yahtzee.com'],
                        ats = ['kkansky','mjackson']
                     )
        Status.fullCreate(tweet)
        

