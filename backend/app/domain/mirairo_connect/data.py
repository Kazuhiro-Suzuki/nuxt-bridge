from dataclasses import dataclass
from datetime import date
from typing import Optional, Type, TypeVar, Generic
from app.utils.dict_util import parse_date_fields, select_fields, get_date_fields, get_fields

T = TypeVar('T')


@dataclass(frozen=True)
class Result(Generic[T]):
    value: Optional[T]
    error: Optional[str]

    @classmethod
    def success(cls, value):
        return cls(value, None)

    @classmethod
    def failure(cls, error: str):
        return cls(None, error)

    def unwrap(self, exception_class: Type[Exception] = Exception) -> T:
        if self.error:
            raise exception_class(self.error)
        return self.value


@dataclass(frozen=True)
class MirairoConnectContext:
    api_base_url: str
    client_id: str
    client_secret: str
    redirect_url_origin: str

    def get_redirect_uri(self, city_code: str) -> str:
        return f'{self.redirect_url_origin}/redirect/mirairo-id/?citycode={city_code}'


@dataclass(frozen=True)
class Connection:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


@dataclass(frozen=True)
class AnonymousCertificate:
    date_of_birth: date
    """生年月日"""
    certificate_type: str
    """障害者手帳種別"""
    barrier_grade: str
    """等級"""
    barrier_variety: str
    """旅客運賃減額"""
    issued_by: str
    """発行元自治体"""
    myna_confirmed: bool
    """マイナポータル連携済み"""
    expiration_date: Optional[date]
    """有効期限"""
    date_of_issue: Optional[date]
    """交付日"""
    date_of_reissue: Optional[date]
    """更新日"""

    @classmethod
    def from_dict(cls, data: dict) -> 'AnonymousCertificate':
        return cls(**select_fields(
            parse_date_fields(data, *get_date_fields(cls)),
            *get_fields(cls),
        ))
