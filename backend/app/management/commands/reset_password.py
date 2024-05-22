from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

from account.models.user import User


class Command(createsuperuser.Command):
    help = './manage.py reset_password --password password --email testest@mail.com'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        # database = options.get('database')
        password = options.get('password')
        # username = options.get('username')
        email = options.get('email')

        # if not password or not username or not email:
        if not password or not email:
            raise CommandError(
                "--email --username and --password are required options")

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        if options.get('verbosity', 0) >= 1:
            self.stdout.write("Reset password successfully.")
