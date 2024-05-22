from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class RegionProfile:
    is_active: bool
    auth_url: str
    client_id: str
    redirect_url_origin: str
    # クライアントにわたす情報なので client_secret を含めてはいけない

    @classmethod
    def default(cls):
        return cls(
            False,
            '',
            '',
            '',
        )


@dataclass(frozen=True)
class UserConnection:
    connected_at: datetime
    # あとでユーザの連携状況のデータを追加する


@dataclass(frozen=True)
class MirairoConnectViewModel:
    """
    ミライロ連携画面の初期化データ
    """
    region_profile: RegionProfile
    user_connection: Optional[UserConnection]
