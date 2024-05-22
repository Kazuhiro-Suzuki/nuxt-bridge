from django.core.management.base import CommandError
from django.contrib.auth.management.commands import createsuperuser

from account.models.user import User
from account.models.user_profile import PartitionedUserProfile
from app.models.region import Region


class Command(createsuperuser.Command):
    help = './manage.py create_superuser --password password --email testest@mail.com --city_code 131032'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--password', dest='password', type=str,)
        parser.add_argument('--city_code', dest='city_code', type=int)


    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        email = options.get('email')
        password = options.get('password')
        city_code = options.get('city_code')

        if not password or not email or not city_code:
            raise CommandError("--email, --password and --city_code are required options")

        try:
            region = Region.objects.get(city_code=city_code)
            user_data = {
                'password': password,
                'email': email,
            }
        
            user = User.objects.create_superuser(**user_data)

            PartitionedUserProfile.objects.create(
                uid=user.uid,
                email=user.email,
                user=user,
                region=region,
            )

            if options.get('verbosity', 0) >= 1:
                self.stdout.write("Superuser created successfully.")
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
