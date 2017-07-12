from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    help = ''

    def add_arguments(self, parser):
        parser.add_argument('user_name',type=str)

    def handle(self, *args, **options):
        pass
    pass