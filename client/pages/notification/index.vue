<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="12" md="8" lg="8" xl="8">
        <v-card outlined elevation="1">
          <DenseToolBar
            :baseColor="regionData.base_color"
            title="検索"
          />
          <v-card-text>
            <v-text-field
              v-model="searchWord"
              label="キーワードを入力してください"
            ></v-text-field>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="12" md="8" lg="8" xl="8">
        <NotificationList
          :searchWord="searchWord"
          :items="items"
          :citycode="citycode"
          :title="title"
          :baseColor="regionData.base_color"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {mapGetters} from "vuex";
import { pageTitle } from '@/model/pageTitle'

export default {
  head() {
    return {
      title: this.title
    }
  },
  data() {
    return {
      title: "お知らせ一覧",
      citycode: this.$route.query.citycode,
      items: [],
      searchWord: "",
    }
  },
  async asyncData({ route, $api }) {
    let items = []
    let errorMessage = ''
    const response = await $api.getPublicNotification(`city_code=${route.query.citycode}`)
    // console.log(response)
    if (response.status == 200) {
      items = response.data
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = ''
      }
    }
    return {
      items,
      errorMessage,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
  methods: {
    activateLink(pattern) {
      /*
      bodyを改行で分割して、一文ずつリンクがあるか確認
      リンクがある分は、マッチしてaタグの文字列と変換
      */
      let re = new RegExp(pattern)
      for (let i = 0; i < this.items.length; i++) {
        if (re.test(this.items[i].body)) {
          let newBody = ''
          let bodyList = this.items[i].body.split('\n')
          for (let j = 0; j < bodyList.length; j++) {
            let include_url = re.test(bodyList[j])
            if (include_url) {
              // console.log(bodyList[j])
              let result = bodyList[j].match(pattern)
              let link = result[0]
              if (pattern.includes('http')) {
                // URLの場合
                if(link.includes('](http')){
                  newBody = newBody + bodyList[j] + '\n'
                }else{
                  let a_link = `<a href="${link}" target="_blank">${link}</a>`
                  newBody = newBody + bodyList[j].replace(link, a_link) + '\n'
                }
              } else if (pattern.includes('@')) {
                // メールアドレスの場合
                let a_link = `<a href="mailto:${link}">${link}</a>`
                newBody = newBody + bodyList[j].replace(link, a_link) + '\n'
              } else if (pattern.includes('{4}')) {
                // 電話番号の場合
                let a_link = `<a href="tel:${link}">${link}</a>`
                newBody = newBody + bodyList[j].replace(link, a_link) + '\n'
              }
            } else {
              newBody = newBody + bodyList[j] + '\n'
            }
          }
          this.items[i].body = newBody
        }
      }
    },
  },
  created() {
    /*
      リンク有効化の条件
      - URL
        - http or httpsから始まること
        - URL最後に改行が入ること
        - 一文に一つまで（複数不可）
      - Mail
        - @が入ること
        - アドレス最後に改行が入ること
        - 一文に一つまで（複数不可）
      - Tel
        - XX-XXXX-XXXXなどのハイフン表記であること
        - 下4桁が必ず数字であること
        - 一文に一つまで（複数不可）
    */
    this.activateLink('(?<!\\]\\()https?://.*')
    this.activateLink('[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}')
    // this.activateLink('(0[1-9]{1,4}-[0-9]{1,4}-[0-9]{4})')

    let titleInfo = pageTitle.find(item => item.city_code ==  this.citycode);
    this.title = titleInfo.notification_title
  },
}
</script>
