from django.core.management.base import BaseCommand, CommandError
from urlshortner.views import delete_expired_links
import logging
log = logging.getLogger(__name__)


# Command that will update the status of all trips in the database
class Command(BaseCommand):
    help = 'Delete all expired links'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        log.info("Deleting all expired links")
        delete_expired_links()

