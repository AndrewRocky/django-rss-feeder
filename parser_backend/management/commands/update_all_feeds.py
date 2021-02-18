from parser_backend.models import Feed, Post
from parser_backend.update_feeds import update_feed
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Updates all feeds.'

    def add_arguments(self, parser):
        parser.add_argument('arr', type=str)

    def handle(self, *args, **options):
        feed_list = Feed.objects.all()
        feed_url_list = [feed.url for feed in feed_list]
        for feed_url in feed_url_list:
            update_feed(feed_url)