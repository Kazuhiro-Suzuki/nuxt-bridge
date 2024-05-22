from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from account.repositories import account_repository
from app.models import Region, Facility, FacilityCategory
from app.views.facility_view import FacilityView, FacilityPublicView


User = get_user_model()


def set_up_test_data():
    user = User.objects.create_user(
        email='test-user@gmail.com',
        password='test',
        phone_number='123456',
        type='general_user'
    )

    (token, _, _) = account_repository.generate_jwt(
        email=user.email,
        type=user.type,
        city_code='131032'
    )

    region = Region.objects.create(
        name='Minato City',
        city_code='131032',
        email='lg.pwd.minato@gmail.com',
        header_text='みなと障害者支援アプリ',
        header_image='image-minato.png',
        top_image='top4-minato.jpg',
        base_color='purple',
    )

    category = FacilityCategory.objects.create(
        name = '短期入所',
        contents = '在宅の常時介護を必要とする障害者（児）のいる家庭で、介護を行う者の疾病その他の理由がある場合に、短期間、夜間も含め、障害者（児）の入浴、排せつ又は食事等の介護を行います。',
        created_at = '2021-09-09 12:34:56.789'
    )

    Facility.objects.create(
        region=region,
        name="みなとワークアクティ",
        address="",
        facility_type="disabled_facility",
        category=category,
        postal_code="",
        phone_number="03-5439-8057",
        fax_number="03-5439-8058",
        google_map="https://www.google.com/maps/search/?api=1&query=35.6515442,139.7534082",
        contact="障害保健福祉センター　みなとワークアクティ",
        business_description="就労継続支援Ｂ型事業",
        contents="一般企業等に就職することが困難な知的障害者に、生産活動を提供し、地域社会で豊かな生活を送れるよう自立を支援します。生産活動の内容は、製菓 ・受注・公園清掃・販売活動です。",
        target="18歳以上の知的障害者で原則として単独通所が可能であり、かつ、作業能力があるまたは期待できる人",
        created_at="2021-09-09 12:34:56.789"
    )

    return user, token


class FacilityViewTest(TestCase):
    def setUp(self):
        self.user, self.token = set_up_test_data()
        self.url = '/api/v1/app/facility/'
        self.client = APIRequestFactory()
        self.view = FacilityView.as_view()

    def test_201_creation_ok(self):
        request = self.client.post(self.url, {
            "city_code": "131032",
            "postal_code": "11111",
            "phone_number": "03-5439-8059",
            "name": "工房アミ",
            "address": "〒105-0014 港区芝1-8-23 障害保健福祉センター内"
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_500_serializer_error(self):
        request = self.client.post(self.url, {
            "city_code": "131032",
            "postal_code": "",
            "phone_number": "03-5439-8059",
            "name": "工房アミ",
            "address": ""
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_post_invalid_city_code(self):
        request = self.client.post(self.url, {
            "city_code": "131031",
            "postal_code": "11111",
            "phone_number": "03-5439-8059",
            "name": "工房アミ",
            "address": "〒105-0014 港区芝1-8-23 障害保健福祉センター内"
        })
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_200_put_ok(self):
        request = self.client.put(self.url + '1/', {
            "name": "Update-みなとワークアクティ",
        })

        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_204_delete_ok(self):
        request = self.client.delete('/api/v1/app/facility/1/')
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class FacilityPublicViewTest(TestCase):
    def setUp(self):
        set_up_test_data()
        self.url = '/api/v1/app/facility/public/'
        self.client = APIRequestFactory()
        self.view = FacilityPublicView.as_view()

    def test_200_get_by_id_ok(self):
        request = self.client.get(self.url, {
            "facility_id": "1",
        })
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_200_get_by_facility_type_and_city_code_ok(self):
        request = self.client.get(self.url, {
            'city_code': "131032",
            'facility_type': 'disabled_facility'
        })
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_500_get_invalid_facility_id(self):
        request = self.client.get(self.url, {
            "facility_id": "3",
        })
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_no_facility_type_and_city_code(self):
        request = self.client.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_invalid_city_code(self):
        request = self.client.get(self.url, {
            'city_code': "111111",
            'facility_type': 'disabled_facility'
        })
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
