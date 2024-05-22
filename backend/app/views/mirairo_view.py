import logging

from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from app.utils.dict_util import dataclass_as_dict
from utils.auth import JWTGeneralUserAuthentication, ContinuableJWTGeneralUserAuthentication
from app.use_cases import mirairo as use_cases

logger = logging.getLogger(__name__)


class MirairoConnectInitialDataView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [ContinuableJWTGeneralUserAuthentication, ]
    permission_classes = [AllowAny, ]

    def get(self, request: Request) -> Response:
        """
        ミライロ連携画面の初期表示に必要な情報をまとめて返す
        """
        city_code = request.query_params.get('city_code')
        view_model = use_cases.get_mirairo_connect_initial_data(city_code, request.user)
        if view_model is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data=dataclass_as_dict(view_model), status=status.HTTP_200_OK)


class MirairoConnectView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTGeneralUserAuthentication, ]

    def post(self, request: Request) -> Response:
        """
        ミライロ連携コードを受け取ってアクセストークンを取得する
        アクセストークンを使ってミライロID情報を取得する
        """
        use_cases.connect_to_mirairo_id(request.user, request.data['code'])
        return Response(status=status.HTTP_201_CREATED)


class MirairoDisconnectView(APIView):
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTGeneralUserAuthentication, ]

    def post(self, request: Request) -> Response:
        """
        ミライロ連携トークンおよび連携により取得した情報をすべて削除する
        """
        use_cases.disconnect_from_mirairo_id(request.user)
        return Response(status=status.HTTP_200_OK)
