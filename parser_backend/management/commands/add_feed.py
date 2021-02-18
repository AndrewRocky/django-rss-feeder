from parser_backend.models import Feed, Post
from parser_backend.add_feed import new
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Updates all feeds.'

    def add_arguments(self, parser):
        parser.add_argument('feed_url', type=str)

    def handle(self, *args, **options):
        #try:
        new(options['feed_url'])
        """ except:
            raise CommandError('Error when adding new Feed') """
        self.stdout.write(self.style.SUCCESS('Successfully added new feed'))
