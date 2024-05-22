CONTENT = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/@mdi/font@4.x/css/materialdesignicons.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
  <meta http-equiv="content-type" charset="UTF-8">
</head>
<body>
  <div id="app">
    <v-app dark>
      <v-app-bar :clipped-left="true" fixed app color="indigo darken2">
        <v-toolbar-title class="font-weight-bold white--text">
          障害者支援サービス
        </v-toolbar-title>
      </v-app-bar>
      <v-main>
        <v-container full-height fluid>
          <v-row justify="center">
            <v-card width="450" class="mt-15 pa-3">
              <v-row justify="center">
                <h2 class="mt-10 mb-8 primary--text">メンテナンス中</h2>
                <h3 class="mb-0">2021/6/24 20:00 〜 2021/7/8 00:00</h3>
                <p>※作業状況により、時間が前後する場合がございます。</p>
              </v-row>
              <v-card-text>
                <p>いつもご利用いただき、ありがとうございます。</p>
                <p>このたびサービス向上のため、システムメンテナンスを実施致します。</p>
                <p>大変ご迷惑をお掛け致しますが、何卒ご理解頂きますようよろしくお願い申し上げます。</p>
              </v-card-text>
            </v-card>
          </row>  
        </v-container>
      </v-main>
      <v-footer :absolute="false" app>
        <span>&copy; {{ new Date().getFullYear() }}</span>
      </v-footer>
    </v-app>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
  <script>
    new Vue({
      el: '#app',
      vuetify: new Vuetify(),
    })
  </script>
</body>
</html>
 """


def lambda_handler(event, context):
    # Generate HTTP OK response using 200 status code with HTML body.
    # ssm = boto3.client('ssm', region_name="us-east-1")
    # ssm_response = ssm.get_parameters(
    #     Names=[
    #         '/dd-support/prod/white_ip_addresses'
    #     ]
    # )
    # allowed_ip_addresses = ssm_response['Parameters'][0]['Value'].split(',')
    allowed_ip_addresses = "${white_ip_addresses}"
    allowed_ip_addresses = allowed_ip_addresses.split(',')

    request = event['Records'][0]['cf']['request']
    client_ip = request['clientIp']

    if client_ip in allowed_ip_addresses:
        return request
    else:
        response = {
            'status': '200',
            'statusDescription': 'OK',
            'headers': {
                "content-type": [
                    {
                        'key': 'Content-Type',
                        'value': 'text/html'
                    }
                ]
            },
            'body': CONTENT
        }

        return response
