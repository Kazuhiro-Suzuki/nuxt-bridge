import logging
import threading
import traceback
import uuid
from typing import Optional

from django.http import HttpRequest

# from app.views.authorization import extract_login_id_city_code
from .string_util import random_str

local = threading.local()


__all__ = [
    'RequestIdLoggingMiddleware',
    'CommonNameLoggingMiddleware',
    'LoginIdLoggingFilter',
    'CityCodeLoggingFilter',
    'IsOfficeStaffLoggingFilter',
    'RequestIdLoggingFilter',
    'CommonNameLoggingFilter',
    'IpAddressForLoggingFilter',
    'TaskIdLoggingFilter',
    'format_error_single_line',
]


def format_error_single_line(e: BaseException) -> str:
    trace = traceback.format_exc().strip().replace('\n', ' -> ')
    return f'err={e.__class__.__name__}: {e} trace={trace}'


class HeaderLoggingMiddlewareBase:
    """
    log にHTTPリクエストヘッダを出力するカスタム項目を取得または生成する Middleware の基底クラス
    """
    header_name = ''
    field_name = ''

    def __init__(self, get_response):
        self.get_response = get_response

    def get_header_value(self, request):
        if self.header_name in request.headers:
            return request.headers[self.header_name]
        return None

    def __call__(self, request: HttpRequest):
        setattr(local, self.field_name, self.get_header_value(request))
        response = self.get_response(request)
        # response時はクリアしておく
        setattr(local, self.field_name, None)
        return response


class RequestIdLoggingMiddleware(HeaderLoggingMiddlewareBase):
    """
    log に rid を出力するカスタム項目を取得または生成する Middleware
    X-Amzn-Trace-Id (ALBが自動でつけてくれるヘッダ) があればその値を取得する。
    次に X-Request-Id カスタムリクエストヘッダがあればその値を取得する
    なければ自動生成する
    """
    header_name = 'X-Request-Id'
    trace_header_name = 'X-Amzn-Trace-Id'
    field_name = 'rid'

    def get_header_value(self, request):
        if self.trace_header_name in request.headers:
            return request.headers[self.trace_header_name]
        if self.header_name in request.headers:
            return request.headers[self.header_name]
        return str(uuid.uuid4())


class CommonNameLoggingMiddleware(HeaderLoggingMiddlewareBase):
    """
    log にクライアント証明書のCN値を出力するカスタム項目を取得する Middleware
    X-Common-Name カスタムリクエストヘッダがあればその値を取得する
    """
    header_name = 'X-Common-Name'
    field_name = 'cn'


class IpAddressLoggingMiddleware(HeaderLoggingMiddlewareBase):
    """
    log にクライアント証明書のCN値を出力するカスタム項目を取得する Middleware
    X-Forwarded-For リクエストヘッダがあればその値を取得する
    """
    header_name = 'X-Forwarded-For'
    field_name = 'ip'

    def get_header_value(self, request):
        if self.header_name in request.headers:
            return request.headers[self.header_name]
        return request.META.get('REMOTE_ADDR')


class CustomAttrFilterBase(logging.Filter):
    field_name = ''

    def filter(self, record):
        setattr(record, self.field_name, getattr(local, self.field_name, None))
        return True


class LoginIdLoggingFilter(CustomAttrFilterBase):
    field_name = 'login_id'


class CityCodeLoggingFilter(CustomAttrFilterBase):
    field_name = 'city_code'


class IsOfficeStaffLoggingFilter(CustomAttrFilterBase):
    field_name = 'is_office_staff'


class RequestIdLoggingFilter(CustomAttrFilterBase):
    field_name = 'rid'


class CommonNameLoggingFilter(CustomAttrFilterBase):
    field_name = 'cn'


class IpAddressForLoggingFilter(CustomAttrFilterBase):
    field_name = 'ip'


class TaskIdLoggingFilter(CustomAttrFilterBase):
    field_name = 'tid'

    @classmethod
    def set_or_generate(cls, task_id: Optional[str] = None) -> str:
        if task_id is None:
            task_id = random_str(4)
        setattr(local, cls.field_name, task_id)
        return task_id
