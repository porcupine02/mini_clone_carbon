from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.conf import settings
import os
import json


class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        # Load seed data
        seed_file_path = os.path.join(settings.BASE_DIR, 'shared', 'management', 'commands', 'seed_data.json')
        with open(seed_file_path, 'r') as f:
            seed_data = json.load(f)

        # Create groups
        for group_name in seed_data.get('groups', []):
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Create group: {group_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Group already exists: {group_name}'))

        # Create users
        for user_data in seed_data.get('users', []):
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                group = Group.objects.get(name=user_data['group'])
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Create user: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'User already exists: {username}'))
