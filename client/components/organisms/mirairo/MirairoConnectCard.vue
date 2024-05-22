<template>
  <div>
    <v-row class="py-6" v-if="!userConnection">
      <v-col cols="12" class="d-flex justify-center">
        <v-btn
          x-large
          elevation="1"
          color="white"
          class="text-h6"
          :href="connectionUrl"
        >
          ミライロID登録済みの方はこちら
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
            未登録の方はこちら
          </v-btn>
        </div>
        <div class="text-center caption pt-2">※外部サイトに遷移します</div>
      </v-col>
    </v-row>
    <v-row class="py-6" v-else>
      <v-col cols="12" class="d-flex justify-center">
        <v-btn
          x-large
          elevation="1"
          color="white"
          class="text-h6"
          :href="applicationUrl"
          target="_blank"
        >
          ミライロIDへ
        </v-btn>
      </v-col>
      <v-col cols="12">
        <div class="d-flex justify-center">
          <v-btn
            large
            elevation="1"
            color="grey darken-1"
            dark
            @click="$emit('disconnect')"
          >
            連携解除を希望の方はこちら
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <div v-if="test">
      <v-btn @click="testRedirect">test redirect</v-btn>
    </div>
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
    profile: {
      type: Object,
      required: true
    },
    userConnection: {
      type: Object,
      default: null
    },
    citycode: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      test: false
    }
  },
  computed: {
    connectionUrl() {
      // ミライロ連携URLを生成
      const authUrl = this.profile.authUrl
      const clientId = this.profile.clientId
      const state = `citycode_${this.citycode}`
      const selfBaseUrl = this.profile.redirectUrlOrigin
      const redirectUrl = `${selfBaseUrl}/redirect/mirairo-id/?citycode=${this.citycode}`
      return `${authUrl}/oauth/authorize?client_id=${clientId}&scope=certificate.anonymous&state=${state}&redirect_uri=${redirectUrl}&response_type=code`
    },
    invitationUrl() {
      return "https://mirairo-id.jp/"
    },
    applicationUrl() {
      return "https://mirairoid.page.link/NLtk"
    }
  },
  methods: {
    testRedirect() {
      location.href = `/redirect/mirairo-id?citycode=${this.citycode}&code=test&state=citycode_${this.citycode}`
    }
  }
}
</script>
