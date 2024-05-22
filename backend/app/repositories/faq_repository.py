import logging

from utils import exceptions
from utils import format_error_single_line
from django.forms.models import model_to_dict

from app.models import Region, FAQ, FAQCategory
from app.repositories import region_repositories

logger = logging.getLogger(__name__)


def get_object(city_code: str):
    try:
        region_obj = Region.objects.get(city_code=city_code)
        return FAQ.objects.filter(region_id=region_obj.id)
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500


def get_object_with_category(city_code: str):
    try:
        region_obj = region_repositories.get_object(city_code=city_code)
        categories = FAQCategory.objects.select_related()
        faqs = FAQ.objects.filter(region_id=region_obj.id).order_by('id').select_related('category')

        res = []
        dcit_no_category = {
            'id': None,
            'name': None,
            'faqItems': []
        }
        for category in categories:
            dict = {
                'id': category.id,
                'name': category.name,
                'faqItems': []
            }
            for faq in faqs:
                if faq.category and (category == faq.category):
                    dict['faqItems'].append(model_to_dict(faq))
            if dict['faqItems']:
                res.append(dict)
        
        for faq in faqs:
            if not faq.category:
                dcit_no_category['faqItems'].append(model_to_dict(faq))
        if dcit_no_category['faqItems']:
                res.append(dcit_no_category)
        
        print(res)
        return res  
    except Exception as e:
        logger.error(format_error_single_line(e))
        raise exceptions.Exception500