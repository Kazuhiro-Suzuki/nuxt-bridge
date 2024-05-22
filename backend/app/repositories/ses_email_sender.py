import logging
from typing import Optional

import boto3
from app.models.region import Region
from app.models.notification import Notification
from django.conf import settings
from app.repositories import email_repository

logger = logging.getLogger(__name__)


def make_notification_body(region: Region, notification: Notification) -> str:
    email = email_repository.get_object(region=region)
    if region.city_code in ['131237', '212172', '092134'] :
        body = email.notification_body.replace('notification_subject', notification.subject)
    else:
        body = email.notification_body
    return f"""

{body}
"""

def make_csv_download_body(email: str, region: Region) -> str:
        return f"""

{region.header_text}です。

ユーザー情報が下記の管理者ユーザーによってダウンロードされました。
管理者ユーザー: {email}


※本メールはシステムより自動送信しております。
送信専用のため、このメールにご質問などをご返信いただいてもお答えすることは出来ません。

※本システムに関するお問い合わせ先
{region.department}
電話番号: {region.phone_number}

※配信元
{region.header_text}
{settings.BASE_URL}/home?citycode={region.city_code}
"""

def make_inquiry_body(region: Region) -> str:
    # TODO 複数自治体へサービス展開する際は、regionから情報を取得するように変更が必要
    return f"""

{region.header_text}です。

新しいお問い合わせの返信を受信しました。
お時間がある際に、ぜひご覧ください。


※本メールはシステムより自動送信しております。
送信専用のため、このメールにご質問などをご返信いただいてもお答えすることは出来ません。

※本システムに関するお問い合わせ先
{region.department}
電話番号: {region.phone_number}

※配信元
{region.header_text}
{settings.BASE_URL}/home?citycode={region.city_code}
"""


def make_signup_body(region: Region, uid: str) -> str:
    # TODO 複数自治体へサービス展開する際は、regionから情報を取得するように変更が必要
    return f"""

{region.header_text}です。

会員登録を受付いたしました。
以下URLより、内容の確認と登録を進めてください。

▼会員登録確認ページ
{settings.BASE_URL}/account/signupcomplete?citycode={region.city_code}&uid={uid}

■ご注意
まだ会員登録は完了しておりません。
上記URLから、登録完了までお進みください。


※本メールはシステムより自動送信しております。
送信専用のため、このメールにご質問などをご返信いただいてもお答えすることは出来ません。

※本システムに関するお問い合わせ先
{region.department}
電話番号: {region.phone_number}

※配信元
{region.header_text}
{settings.BASE_URL}/home?citycode={region.city_code}
"""


def make_reset_password_body(region: Region, uid: str) -> str:
    # TODO 複数自治体へサービス展開する際は、regionから情報を取得するように変更が必要
    return f"""

{region.header_text}です。

パスワードリセットを受付しました。
以下URLより、内容の確認と再登録を進めてください。

▼会員登録確認ページ
{settings.BASE_URL}/account/resetpassword?citycode={region.city_code}&uid={uid}

■ご注意
まだパスワードリセットは完了しておりません。
上記URLから、完了までお進みください。


※本メールはシステムより自動送信しております。
送信専用のため、このメールにご質問などをご返信いただいてもお答えすることは出来ません。

※本システムに関するお問い合わせ先
{region.department}
電話番号: {region.phone_number}

※配信元
{region.header_text}
{settings.BASE_URL}/home?citycode={region.city_code}
"""


class Message:
    sender: str
    receiver: str
    subject: str
    body: str
    status: Optional[str]
    ses_response: Optional[dict]


class SesEmailSender:
    @staticmethod
    def send_email(message: Message) -> Message:
        try:
            client = boto3.client(
                'ses',
                region_name=settings.AWS_REGION_NAME
            )

            response = client.send_email(
                Source=message.sender,
                Destination={
                    'ToAddresses': [
                        message.receiver
                    ]
                },
                Message={
                    'Subject': {
                        'Data': message.subject,
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': message.body,
                            'Charset': 'UTF-8'
                        }
                    }
                },
                ConfigurationSetName=settings.AWS_SES_CONFIGURATION_SET_NAME,
            )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                message.status = 'succeeded'
            else:
                message.status = 'failed'

            message.ses_response = response

            return message
        except Exception as e:
            logger.error(e)
            message.status = 'error'

            return message
