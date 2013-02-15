import subprocess
from django.core.management.base import BaseCommand
from ask.models import Asker


class Command(BaseCommand):
    help = """Build audio files."""

    def handle(self, *args, **options):
        for askerref in args:
            for i in Asker.objects.get(reference=askerref).questions():
                file_ = "files/audio/%s.aiff" % (i.question.variable_name, )
                cmd = ['say', i.question.text, "-o", file_]
                subprocess.Popen(cmd)
                print cmd
