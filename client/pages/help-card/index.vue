<template>
  <v-container>
      <v-row justify="center" v-if="$auth.loggedIn">
        <v-col sm="10" md="8" lg="8" xl="8">
           <v-col cols="12">
            <div class="font-weight-bold">氏名</div>
            <div>{{userInfo.last_name + userInfo.first_name}}</div>
          </v-col>
          <v-divider/>
          <v-col cols="12">
            <div class="font-weight-bold">連絡先</div>
            <div>{{userInfo.phone_number}}</div>
          </v-col>
          <v-divider/>
          <v-col cols="12">
            <div class="font-weight-bold">障害・病気等の内容</div>
            <div>{{userInfo.note1}}</div>
          </v-col> 
          <v-divider/>
          <v-col cols="12">
            <div class="font-weight-bold">知ってほしいこと（薬、アレルギー、かかりつけ医など）</div>
            <div>{{userInfo.note2}}</div>
          </v-col> 
          <v-divider/>
          <v-col cols="12">
            <div class="font-weight-bold">配慮事項</div>
            <div 
              v-for="(item, i) in userInfo.disability_category"
              :key="i"
            >
              {{item}}
            </div>
          </v-col>
          <v-divider/>
          <v-col cols="12">
            <div class="font-weight-bold">配慮してほしいこと</div>
            <div>{{userInfo.note3}}</div>
          </v-col> 
          <v-divider/>
          <v-col xs="12" class="d-flex justify-center pt-8">
            <v-btn
              x-large
              elevation="1"
              dark
              class="font-weight-bold"
              :color="regionData.dark_color"
              :loading="downloadingPdf"
              @click="downloadPdf"
            >
              ヘルプカードをダウンロード
            </v-btn>
          </v-col>
        </v-col>
      </v-row>
      <v-row justify="center" v-else>
        <v-col sm="10" md="8" lg="8" xl="8">
          <v-col cols="12">
              <p>ヘルプカードをスマホに登録して、困ったときにいつでも提示することができます。</p>
              <p>カードを持ち歩く必要がないので、紛失する心配もなくなり安心です。</p>
          </v-col>
          <v-col cols="12">
            <div class="bg-help-card-color rounded-lg pa-4">
              <p class="font-weight-bold">ヘルプカードとは？</p>
              <p>障害のある方などが、困ったときに、周りの方に助けをお願いするためのものです。</p>
              <v-btn
                class="font-weight-bold pa-0"
                text
                target="_blank"
                href="https://www.city.edogawa.tokyo.jp/e041/kenko/fukushikaigo/shogaisha/kenriyogo/helpcard.html"
                :color="regionData.dark_color"
              >
                <span class="text-decoration-underline">詳しくはこちら</span>
                <v-icon size="16px" :color="regionData.dark_color">$IconNewwindowLine</v-icon>
              </v-btn>
            </div>
          </v-col>
          <v-col cols="12">
            <div class="d-flex justify-center">
              <v-btn
                  large
                  elevation="1"
                  :to="'/account?citycode='+regionData.city_code"
                  :color="regionData.dark_color"
                  class="font-weight-bold rounded-lg"
                  dark
              >
                  会員登録(ログイン)して利用
              </v-btn>
            </div>
          </v-col>
        </v-col>
     </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  head() {
    return {
      title: 'ヘルプカード',
      readonly: true
    }
  },
  data() {
    return {
      title: 'ヘルプカード',
      downloadingPdf: false
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    })
  },
   methods: {
    // async downloadPdf(){
    //   this.downloadingPdf = true
    //   const pdfCreationResponse = await this.$api.createHelpCardPDF()
    //   if (pdfCreationResponse.status == 200) {
    //     const response = await this.$api.getHelpCardPDF()
    //     const blob = new Blob([res.data], { type: 'application/pdf' })
    //     const fileName = token + '.pdf'
    //     const url = (window.URL || window.webkitURL).createObjectURL(blob)
    //     const link = document.createElement('a')
    //     link.href = url;
    //     a.download = fileName
    //     document.body.appendChild(link);
    //     link.click();
    //     document.body.removeChild(link)

    //     // const url = window.URL.createObjectURL(new Blob([response.data]));
    //     // const link = document.createElement('a');
    //     // link.href = url;
    //     // link.setAttribute('download', 'user-list.csv'); 
    //     // document.body.appendChild(link);
    //     // link.click();
    //     // document.body.removeChild(link)
    //     this.$notifier.showMessage({ content: 'ダウンロードが完了しました。', color: 'info' })
    //   } else{
    //     if (pdfCreationResponse.data.detail) {
    //       errorMessage = pdfCreationResponse.data.detail
    //     } else {
    //       errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
    //     }
    //   }
    // }
    async downloadPdf() {
      this.downloadingPdf = true
      const sleep = msec => new Promise(resolve => setTimeout(resolve, msec))
      try {
        const res = await this.$api.createHelpCardPDF()
        const token = res.data.token
        const id = res.data.id
        while (true) {
          try {
            const response = await this.$api.getHelpCardPDF(`token=${token}&id=${id}`)
            console.log(response);
            window.location.href = response.data
            // const blob = new Blob([response.data], { type: 'application/pdf' })

            // // //追加
            // // const reader = new FileReader();
            // // //追加
            // // reader.onload = function(e) {
            // //     window.location.href = reader.result;
            // // }
            // // //追加
            // // reader.readAsDataURL(blob);

            // const fileName = token + '.pdf'

            // //IE判定
            // if (navigator.msSaveOrOpenBlob) {
            //   navigator.msSaveOrOpenBlob(blob, fileName)
            // } else {
            //   const objectUrl = (window.URL || window.webkitURL).createObjectURL(blob)
            //   const a = document.createElement('a')
            //   a.href = objectUrl
            //   a.download = fileName
            //   document.body.appendChild(a)
            //   a.click()
            //   document.body.removeChild(a)
            // }
            break
          } catch (e) {
            console.log(e)
            await sleep(1000)
          }
        }

      } catch (e) {
        console.log(e)
      }
      this.downloadingPdf = false
    }
  },
  async asyncData({ $api }) {
    let errorMessage = ''
    let userInfo = {}
    const response = await $api.getUserInfo()
    if (response.status = 200) {
      userInfo = response.data
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = ''
      }
    }
    return {
      userInfo,
      errorMessage,
    }
  },
}
</script>

<style scoped>
.bg-help-card-color{
  background-color: #F5F5F5;
}
/* .over-contents{
  margin: 0 calc(50% - 50vw);
	padding: 4px calc(50vw - 50% + 8px);
	width: 100vw;
} */
</style>