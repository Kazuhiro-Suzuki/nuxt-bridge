# lg-pwd

## ローカル開発環境

## 手順
### client
1. clientディレクトリ直下に.envファイルを配置
2. yarn install

### backend
- backendディレクトリ直下に.envファイルを配置 
- docker-compose.yml の postgresリソースのコメントアウトを解除
- accountとappのマイグレーションファイルをそれぞれのmigrations/local直下に全てコピーする
- ローカル用postgres初回起動（時間がかかるとbackendコンテナでエラーが発生する）  
docker-compose up postgres 
- docker-compose up
- docker exec -it lg-pwd_backend bash
- ModuleNotFoundError: No module named 'corsheaders'が発生した場合のみ  
pip install django-cors-headers
- python manage.py migrate
- ./manage.py loaddata app_region.json
- ./manage.py create_superuser --password password --email test@mail.com --city_code 131237
- その他の初期データが必要な場合は、以下を書き換えて実行（backend/app/fixtures）  
./manage.py loaddata 〇〇.json

