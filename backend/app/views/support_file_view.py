import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from account.repositories import account_repository

from utils import exceptions
from app.repositories import support_file_repository
import json

from utils.auth import ContinuableJWTGeneralUserAuthentication, JWTAppUserAuthentication

logger = logging.getLogger(__name__)


class SupportFileView(APIView):#サポートファイル一覧取得
    renderer_classes = [JSONRenderer, ]
    authentication_classes = []
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if 'city_code' not in request.GET:
            raise exceptions.ValidationException
        qs = support_file_repository.get_object(city_code=request.GET['city_code'])
        return Response(data=qs, status=status.HTTP_200_OK)


class SupportFileReplView(APIView):#サポートファイル回答内容
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [ContinuableJWTGeneralUserAuthentication]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if 'form_id' not in request.GET:
            raise exceptions.ValidationException
        qs = support_file_repository.get_repl(user=request.user, form_id=request.GET['form_id'], page_cnt=request.GET.get("page_cnt", "10"), page=request.GET.get("page", "1"))
        return Response(data=qs, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        if 'form_id' not in request.GET:
            raise exceptions.ValidationException
        qs = support_file_repository.set_repl(form_id=request.GET['form_id'], user=request.user, repl=json.loads(request.body.decode()))
        return Response(data=qs, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        if 'id' not in request.GET:
            raise exceptions.ValidationException
        support_file_repository.update_repl(id=request.GET['id'], repl=json.loads(request.body), user=request.user)
        return Response(data="ok", status=status.HTTP_200_OK)


class SupportFileReplIdView(APIView):#サポートファイル回答内容
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [ContinuableJWTGeneralUserAuthentication]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if 'reol_id' not in request.GET:
            raise exceptions.ValidationException
        qs = support_file_repository.get_repl_id(user=request.user, reol_id=request.GET['reol_id'])
        return Response(data=qs, status=status.HTTP_200_OK)


class SupportFileUploadFileView(APIView):#フロント用ファイル保存API
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [ContinuableJWTGeneralUserAuthentication]
    permission_classes = [permissions.AllowAny, ]

    def post(self, request: Request) -> Response:
        if not (files := request.FILES['file']) or 'form_id' not in request.data or 'form_name' not in request.data:
            raise exceptions.ValidationException
        id = support_file_repository.upload_img(user=request.user, form_id=request.data['form_id'], form_name=request.data['form_name'], file=files)
        return Response(data={id}, status=status.HTTP_201_CREATED)


    def get(self, request: Request) -> Response:
        url = support_file_repository.download_img_url(user_id=request.user.uid, id=request.GET['id'])
        return Response(data={url}, status=status.HTTP_201_CREATED)


class SupportFilePDFView(APIView):  # PDF変換
        renderer_classes = [JSONRenderer, ]
        authentication_classes = [ContinuableJWTGeneralUserAuthentication]
        permission_classes = [permissions.AllowAny, ]

        def get(self, request: Request) -> Response:
            if 'support_file_id' not in request.GET:
                raise exceptions.ValidationException
            url = support_file_repository.download_pdf(user=request.user, vuefile=request.GET.get("vuefile", "[]"), support_file_id=request.GET['support_file_id'])
            return Response(data=url, status=status.HTTP_201_CREATED)


class SupportFileFormOutputView(APIView):#帳票出力用API　回答情報
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTAppUserAuthentication, ]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if 'support_file_id' not in request.GET or 'user_id' not in request.GET:
            raise exceptions.ValidationException
        qs = support_file_repository.get_repl_form_output(support_file_id=request.GET['support_file_id'], user_id=request.GET['user_id'])
        return Response(data=qs, status=status.HTTP_200_OK)


class SupportFileFormOutputFileView(APIView):#帳票出力用API　画像ダウンロードURL
    renderer_classes = [JSONRenderer, ]
    authentication_classes = [JWTAppUserAuthentication, ]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request: Request) -> Response:
        if 'file_id' not in request.GET:
            raise exceptions.ValidationException
        qs = support_file_repository.get_repl_file_output(file_id=request.GET['file_id'])
        return Response(data=qs, status=status.HTTP_200_OK)