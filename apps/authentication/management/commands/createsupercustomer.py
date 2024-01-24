from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import gettext_lazy as _

from django.db import Error

from authentication import serializers
from authentication import models


class Command(BaseCommand):
    help = _('Creates a project admin customer')

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        if models.Customer.objects.filter(username=options['username']).exists():
            raise CommandError(_('A customer with this username already exists'))

        data = {
            'username': options['username'],
            'email': f'{options["username"]}@{options["username"]}.dev',
            'password': options['password'],
            'is_staff': True
        }
        serializer: serializers.CustomerSerializer = serializers.CustomerSerializer(data=data)
        if not serializer.is_valid():
            raise CommandError(_('Write a valid username or password'))

        try:
            customer = serializer.save()
            customer.is_superuser = True
            customer.save()

            self.stdout.write(_('Successfully created admin customer!'))

        except Error:
            raise CommandError(_('Occurred an error while creating customer'))
