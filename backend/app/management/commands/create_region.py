# import datetime
import logging

from django.core.management.base import BaseCommand

from app.models.region import Region
from utils import format_error_single_line

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
        Regionモデルの自治体追加コマンド
        ./manage.py create_region 'Minato City' 131032 '2021-08-31' '2050-12-31' lg.pwd.minato@gmail.com \
            image-minato.png top4-minato.jpg みなと障害者支援アプリ purple
    """

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('city_code', type=int, help='131032')
        parser.add_argument('active_since', type=str, help='')
        parser.add_argument('active_until', type=str, help='')
        parser.add_argument('email', type=str)
        parser.add_argument('header_image', type=str)
        parser.add_argument('top_image', type=str)
        parser.add_argument('header_text', type=str)
        parser.add_argument('base_color', type=str)

    def handle(self, *args, **options):
        # active_since = datetime.datetime.strptime(options['active_since'], '%Y-%m-%d')
        # active_until = datetime.datetime.strptime(options['active_until'], '%Y-%m-%d')
        try:
            object = Region.objects.create(
                name=options['name'],
                city_code=options['city_code'],
                # active_since = active_since,
                # active_until = active_until,
                email=options['email'],
                header_text=options['header_text'],
                header_image=options['header_image'],
                top_image=options['top_image'],
                base_color=options['base_color'],
            )
            self.stdout.write(self.style.SUCCESS(f'success {object.name}'))
        except Exception as e:
            logger.error(format_error_single_line(e))
            self.stdout.write(self.style.ERROR('error'))
