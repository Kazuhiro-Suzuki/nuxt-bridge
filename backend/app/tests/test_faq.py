from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from app.models import Region, FAQ


def set_up_test_data():
    region = Region.objects.create(
        name='Minato City',
        city_code='131032',
        email='lg.pwd.minato@gmail.com',
        header_text='みなと障害者支援アプリ',
        header_image='image-minato.png ',
        top_image='top4-minato.jpg',
        base_color='purple',
    )
    FAQ.objects.bulk_create([
        FAQ(region=region, question="このアプリは無料ですか？", answer="はい、無料でご利用できます。ただし、アプリ利用に伴う通信費、パケット代はご自身の負担となります。"),
        FAQ(region=region, question="会員登録しないと使えませんか？", answer="いえ、会員登録をしなくても、ご利用できます。"),
        FAQ(region=region, question="会員登録すると、どんなメリットがありますか？", answer="港区からのお知らせがあった場合、メールでお知らせを受け取ることができます。また、会員登録をすることで、短期入所施設の予約が可能です。"),
        FAQ(region=region, question="紹介されている施設について詳しく知りたい", answer="電話番号が記載されている施設については、直接ご連絡をお願いいたします。"),
        FAQ(region=region, question="短期入所の予約ができない", answer="会員登録はお済みでしょうか？まだ登録がお済みでない場合、会員登録をし、本アプリにログインをすることで、短期入所の予約ができるようになります。"),
    ])


class FaqViewTest(TestCase):
    def setUp(self):
        set_up_test_data()
        self.url = '/api/v1/app/faq/'
        self.client = APIClient()

    def test_500_get_no_city_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_500_get_invalid_city_code(self):
        response = self.client.get(self.url, {'city_code': '111111'})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_200_get_ok(self):
        response = self.client.get(self.url, {'city_code': '131032'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data[0], {
            "id": 1,
            "region_id": 1,
            "question": "このアプリは無料ですか？",
            "answer": "はい、無料でご利用できます。ただし、アプリ利用に伴う通信費、パケット代はご自身の負担となります。"
        })
        self.assertDictEqual(response.data[1], {
            "id": 2,
            "region_id": 1,
            "question": "会員登録しないと使えませんか？",
            "answer": "いえ、会員登録をしなくても、ご利用できます。"
        })
        self.assertDictEqual(response.data[2], {
            "id": 3,
            "region_id": 1,
            "question": "会員登録すると、どんなメリットがありますか？",
            "answer": "港区からのお知らせがあった場合、メールでお知らせを受け取ることができます。また、会員登録をすることで、短期入所施設の予約が可能です。"
        })
        self.assertDictEqual(response.data[3], {
            "id": 4,
            "region_id": 1,
            "question": "紹介されている施設について詳しく知りたい",
            "answer": "電話番号が記載されている施設については、直接ご連絡をお願いいたします。"
        })
        self.assertDictEqual(response.data[4], {
            "id": 5,
            "region_id": 1,
            "question": "短期入所の予約ができない",
            "answer": "会員登録はお済みでしょうか？まだ登録がお済みでない場合、会員登録をし、本アプリにログインをすることで、短期入所の予約ができるようになります。"
        })
