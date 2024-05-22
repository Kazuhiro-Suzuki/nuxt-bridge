<template>
  <div>
    <v-row class="py-6">
      <v-col cols="12" class="d-flex justify-center">
        <p class="text-center">
          本サービスに登録・ログイン後<br>ミライロIDと連携することができます。
        </p>
      </v-col>
      <v-col cols="12" class="d-flex justify-center">
        <v-btn
          large
          elevation="1"
          target="_blank"
          color="white"
          @click="goToLoginPage"
        >
          ログイン・会員登録
        </v-btn>
      </v-col>
      <v-col cols="12">
        <div class="d-flex justify-center">
          <v-btn
            large
            elevation="1"
            :href="invitationUrl"
            target="_blank"
            color="grey darken-1"
            dark
          >
            ミライロID公式サイトへ
          </v-btn>
        </div>
        <div class="text-center caption pt-2">※外部サイトに遷移します</div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'MirairoConnectCard',
  props: {
    baseColor: {
      type: String,
      required: true,
    },
    citycode: {
      type: String,
      required: true
    }
  },
  data() {
    return {}
  },
  computed: {
    invitationUrl() {
      return "https://mirairo-id.jp/"
    }
  },
  methods: {
    goToLoginPage() {
      this.$router.push(`/account?citycode=${this.citycode}`)
    },
  }
}
</script>
