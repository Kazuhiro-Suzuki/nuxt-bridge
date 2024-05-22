from rest_framework.exceptions import APIException


class ErrorMessage:
    FAILED_CREATE_ACCOUNT = '会員登録ができませんでした、入力内容を確認してくださいa'
    FAILED_CREATE_ACCOUNT_B = '会員登録ができませんでした、入力内容を確認してくださいb'
    FAILED_CREATE_ACCOUNT_C = '会員登録ができませんでした、入力内容を確認してくださいc'
    FAILED_EXEC_ACCOUNT = 'アカウント処理の実行ができませんでした。'
    CHECK_URL = 'URLを確認してください。'
    NO_USER = '該当するメールアドレスのユーザーは存在しません。'
    INCORRECT_REGION_USER = '該当するメールアドレスのユーザーはこの自治体では登録されていません。'
    FAILED_GET_USER_LIST = 'ユーザを取得できませんでした。'
    FAILED_UPDATE_USER_INFO = 'ユーザ情報を更新できませんでした。'
    FAILED_DELETE_USER_INFO = 'ユーザ情報を削除できませんでした。'
    FAILED_GET_REGION = '自治体情報を取得できませんでした。'
    FAILED_GET_NOTIFICATION = 'お知らせデータを取得できませんでした。'
    FAILED_POST_NOTIFICATION = 'お知らせデータを登録できませんでした。'
    FAILED_UPDATE_NOTIFICATION = 'お知らせデータを更新できませんでした。'
    FAILED_DELETE_NOTIFICATION = 'お知らせデータを削除できませんでした。'
    FAILED_GET_FILE = 'ファイルを取得できませんでした。'
    FAILED_POST_FILE = 'ファイルをアップロードできませんでした。'
    FAILED_DELETE_FILE = 'ファイルを削除できませんでした。'
    FACILITY = '施設情報の処理を実行できませんでした。'
    FAILED_POST_FACILITY = '施設を登録できませんでした。'
    FAILED_UPDATE_FACILITY = '施設情報を更新できませんでした。'
    FAILED_DELETE_FACILITY = '施設情報を削除できませんでした。'
    INQUIRY = 'お問い合わせデータの処理を実行できませんでした。'
    ONLY_NUMBER_POLICY = '電話, FAX番号は数字のみで入力してください'
    PASSWORD_RECONFIRM = 'パスワードとパスワード再確認が一致しません。'
    PASSWORD_POLICY = 'パスワードは、半角数字及び大文字小文字の半角英字を含む8文字以上50文字以下で入力してください'
    ALREADY_EXIST = '入力された情報は既に登録されています。'
    FAILED_SEND_EMAIL = 'メールの送信ができませんでした。'
    EXPIRED_URL = 'このURLは有効期限切れです。'
    INCORRECT_PASSWORD = 'パスワードが正しくありません。'
    INVALID_ACCOUNT = 'このアカウントは有効でありません。'
    ALREADY_VALID_ACCOUNT = 'このアカウントは既に有効です。'
    FAILED_GET_SLOT = '予約枠情報を取得できませんでした。'
    FAILED_FIND_SLOT = '予約枠情報を検索できませんでした。'
    FAILED_RESERVE_TEMP_SLOT = '仮予約できませんでした。'
    FAILED_CANCEL_TEMP_SLOT = '仮予約をキャンセルできませんでした。'
    FAILED_GET_TEMP_SLOT = '仮予約情報を取得できませんでした。'
    INVALID_AUTH_INFO = '認証情報が不正です。'
    FAILED_GET_FACILITY = '施設情報を取得できませんでした。'
    FAILED_CREATE_RESERVE = '予約できませんでした。'
    FAILED_CANCEL_RESERVE = '予約キャンセルできませんでした。'
    FAILED_GET_RESERVE = '予約情報を取得できませんでした。'
    FAILED_POST_F_TOKEN = 'デバイストークンを登録できませんでした。'
    NOT_FROM_APP = 'アプリからのアクセスでありません。'


class Exception500(APIException):
    status_code = 500
    default_detail = '500 Internal Server Error. サーバーエラーです、時間を置いてやり直してください。'


class ValidationException(APIException):
    status_code = 500
    default_detail = '500 Internal Server Error. 入力データに不備があります、内容を確認してください。'


class Exception401(APIException):
    status_code = 401
    default_detail = '401 Unauthorized. 認証エラーです。'


class Exception403(APIException):
    status_code = 403
    default_detail = '403 Forbidden Error. 実行権限がありません。'


class Exception503(APIException):
    status_code = 503
    default_detail = '503 Service Unavailable. サービスが利用できません。'
