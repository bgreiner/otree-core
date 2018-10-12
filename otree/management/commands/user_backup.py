from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = (
        "Saves current users before reset")

    def backup_users(self):
        self.stdout.write('Creating user backup file...')
        try:
            with open('users.json', 'w') as f:
                self.stdout.write('File created successfully!')
                self.stdout.write('Retrieving user data...')
                try:
                    call_command('dumpdata', 'auth.user', stdout=f)
                    self.stdout.write('User data saved.')
                except:
                    self.stdout.write('There was a problem accessing user data.')
        except:
            self.stdout.write('File creation failed.')


    def handle(self, **options):
        self.backup_users()



