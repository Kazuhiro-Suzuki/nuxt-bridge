from rest_framework.request import Request
from rest_framework.authentication import BaseAuthentication

from utils import exceptions
from account.repositories import account_repository
from utils.exceptions import Exception401


class JWTAppUserAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        try:
            # get_token はトークンが取れないとすぐに 401 エラーを投げるので一旦キャッチする
            # そうしないとほかの Authentication に処理が移る前に 401 が返ってしまう
            token = account_repository.get_token(headers=dict(request.headers))
        except Exception401:
            return None
        user = account_repository.retrieve_user_from_token(token=token)
        return (user, None)


class JWTGeneralUserAuthentication(BaseAuthentication):
    # Permission なしにこの認証に失敗すると401が返るため注意
    def authenticate(self, request: Request):
        token = account_repository.get_token(headers=dict(request.headers))
        user = account_repository.retrieve_user_from_token(token=token)
        if user.partitioneduserprofile_set.get().account_type != 'general':
            raise exceptions.Exception403
        return (user, None)


class ContinuableJWTGeneralUserAuthentication(BaseAuthentication):
    # Permission と組み合わせて使う用
    def authenticate(self, request: Request):
        try:
            # get_token はトークンが取れないとすぐに 401 エラーを投げるので一旦キャッチする
            # そうしないとほかの Authentication に処理が移る前に 401 が返ってしまう
            token = account_repository.get_token(headers=dict(request.headers))
        except Exception401:
            return None
        user = account_repository.retrieve_user_from_token(token=token)
        if user.partitioneduserprofile_set.get().account_type != 'general':
            raise exceptions.Exception403
        return (user, None)


class JWTBusinessUserAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        token = account_repository.get_token(headers=dict(request.headers))
        user = account_repository.retrieve_user_from_token(token=token)
        if user.partitioneduserprofile_set.get().account_type != 'business':
            raise exceptions.Exception403
        return (user, None)


class JWTSuperUserAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        token = account_repository.get_token(headers=dict(request.headers))
        user = account_repository.retrieve_user_from_token(token=token)
        if not user.is_superuser and user.is_staff and user.partitioneduserprofile_set.get().account_type == 'business':
            raise exceptions.Exception403
        return (user, None)


class JWTGeneralOrFacilityUserAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        token = account_repository.get_token(headers=dict(request.headers))
        user = account_repository.retrieve_user_from_token(token=token)
        if user.partitioneduserprofile_set.get().account_type == 'business':
            raise exceptions.Exception403
        return (user, None)
