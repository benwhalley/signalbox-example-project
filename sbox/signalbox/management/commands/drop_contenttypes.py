from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType


class Command(NoArgsCommand):
    help = """Drops all content types which can be useful when loading fixtures.
    """

    def handle_noargs(self, *args, **options):
        ContentType.objects.all().delete()
        return "Done\n"
