# management/commands/runserver.py

import subprocess
from django.core.management.commands.runserver import Command as RunserverCommand

class Command(RunserverCommand):
    def handle(self, *args, **options):
        self.stdout.write('Starting Webpack in watch mode...')
        subprocess.Popen(['npm', 'run', 'watch:js'], shell=True)
        super().handle(*args, **options)
