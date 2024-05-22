<template>
  <v-container>
    <v-row justify="center" class="py-6">
      <v-col cols="12" class="py-6 d-flex justify-center">
        <div class="d-flex align-center justify-center">
            <span class="headline">Slack（スラック）チャットで情報交換</span>
        </div>
      </v-col>
      <v-col cols="12">
        <p class="text-center">
          意見交換の場として、slackをご活用ください。<br>
          ※招待メールを受け取っている方のみ、確認が可能となります。
        </p>
      </v-col>
      <v-col cols="12" class="py-6">
        <div class="d-flex justify-center">
            <v-btn
                large
                elevation="1"
                color="white"
                :href="slackGuideUrl"
                target="_blank"
            >
                Slackの使用方法の説明
            </v-btn>
        </div>
        <div class="text-center caption pt-2">※外部サイトに遷移します</div>
      </v-col>
      <v-col cols="12" class="py-6">
        <div class="d-flex justify-center">
            <v-btn
                large
                elevation="1"
                :href="invitationUrl"
                target="_blank"
                color="grey darken-1"
                dark
            >
                Slackのサイトへ
            </v-btn>
        </div>
        <div class="text-center caption pt-2">※外部サイトに遷移します</div>
      </v-col>
        
    </v-row>
  </v-container>
</template>

<script>
export default {
  head() {
    return {
      title: 'Slack管理'
    }
  },
  data() {
    return {
      slackPdfUrl: '',
      title: 'Slack管理',
    }
  },
  computed: {
    slackGuideUrl() {
      return "https://d3n2js5ykzz1af.cloudfront.net/"
    },
    invitationUrl() {
      return "https://w1659506093-yrx271683.slack.com/"
    }
  },
  // methods: {
  //   async showPDF() {
  //     const response = await this.$axios.$get('/api/v1/app/information_file/?name=slack.pdf',  { responseType: 'blob' })
  //       .then((response) => {
  //         // console.log(response);
  //         const file = new Blob([response], { type: 'application/pdf' });
  //         const fileURL = URL.createObjectURL(file);
  //         window.open(fileURL);
  //       })
  //       .catch((error) => {
  //         console.error(error);
  //       });
  //   }
  // }
}
</script>