from typing import List

import requests
from django.conf import settings

from app.domain.mirairo_connect.data import Result, Connection, MirairoConnectContext, AnonymousCertificate


def request_connection(code: str, redirect_uri: str, context: MirairoConnectContext) -> Result[Connection]:
    """
    クライアント側で受け取った認可コードでアクセストークンを要求する
    """
    try:
        res = requests.post(
            url=context.api_base_url + '/oauth/token',
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri,
                'client_id': context.client_id,
                'client_secret': context.client_secret,
            }
        )
        if settings.DEBUG:
            print(res.text)
        data = res.json()
        if 'error' in data:
            return Result.failure(data['error'])
        return Result.success(Connection(**data))
    except requests.ConnectionError:
        return Result.failure("connection error")
    except requests.Timeout:
        return Result.failure("connection timeout")


def revoke_connection(connection: Connection, context: MirairoConnectContext) -> Result[None]:
    """
    アクセストークンを無効化する
    """
    try:
        res = requests.get(
            url=context.api_base_url + '/oauth/token/revoke',
            headers={
                'Authorization': f"Bearer {connection.access_token}"
            }
        )
        if settings.DEBUG:
            print(res.text)
        data = res.json()
        if 'error' in data:
            return Result.failure(data['error'])
        return Result.success(None)
    except requests.ConnectionError:
        return Result.failure("connection error")
    except requests.Timeout:
        return Result.failure("connection timeout")


def request_certificates(connection: Connection, context: MirairoConnectContext) -> Result[List[AnonymousCertificate]]:
    """
    ミライロIDのユーザ情報を取得する
    """
    try:
        res = requests.get(
            url=context.api_base_url + '/certificates',
            headers={
                'Authorization': f"Bearer {connection.access_token}"
            }
        )
        if res.status_code == 401:
            return Result.failure("invalid token")
        if settings.DEBUG:
            print(res.text)
        data = res.json()
        return Result.success([AnonymousCertificate.from_dict(cert) for cert in data])
    except requests.ConnectionError:
        return Result.failure("connection error")
    except requests.Timeout:
        return Result.failure("connection timeout")
