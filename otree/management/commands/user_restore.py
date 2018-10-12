import logging
import six
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connections, transaction
from otree import common_internal
from django.core.files import File


class Command(BaseCommand):
    help = (
        "Restores current users after reset")

    def reset_users(self):
        self.stdout.write('Restoring users...')
        try:
            call_command('loaddata', 'users.json')
            self.stdout.write('Restore successful.')
        except:
            self.stdout.write('Restore failed.')

    def handle(self, **options):
        self.reset_users()



