from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates a default superuser if none exists'

    def handle(self, *args, **options):
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists. Skipping creation.')
            )
            return

        # Create default superuser
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@jsitcomp.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser: {user.username}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Default credentials: admin / admin123 - Please change these in production!'
                )
            )
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR('Failed to create superuser. User might already exist.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            ) 