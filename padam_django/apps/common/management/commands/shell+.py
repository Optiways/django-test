import os
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = (
        "Runs iPython with the autoreload activated and some useful modules imported (re, json...)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--pdb",
            dest="pdb",
            action="store_true",
            help="Go into debugging mode when an exception is raised",
        )

    def handle(self, **options):
        arguments = [f"--config='{settings.BASE_DIR}/shell_plus.py'"]
        if options["pdb"]:
            arguments.append("--pdb")
        from IPython import start_ipython

        start_ipython(argv=arguments)