<template>
  <v-container>
    <v-row>
      <v-col>
        <ErrorAlert :message="errorMessage" />
      </v-col>
    </v-row>
    <v-row justify="center" v-if="!errorMessage">
      <v-col sm="8" md="6" lg="6" xl="6">
        <Confirmation
          :title="title"
          :baseColor="baseColor"
          buttonText="ホームに戻る"
          @clickEvent2="$router.push(`/home?citycode=${citycode}`)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  head() {
    return {
      title: '登録完了'
    }
  },
  data() {
    return {
      title: '登録完了',
      errorMessage: '',
      citycode: this.$route.query.citycode,
      baseColor: '',
      data: {
        uid: this.$route.query.uid,
        city_code: this.$route.query.citycode,
      },
    }
  },
  methods: {
    async activate() {
      const response = await this.$api.postActivateAccount(this.data)
      // console.log(response)
      if (response.status == 200) {
        this.$notifier.showMessage({ content: '会員登録が完了しました。', color: 'info' })
      } else {
        if (response.data.detail) {
          this.errorMessage = response.data.detail
        } else {
          this.errorMessage = '会員登録が完了できませんでした、時間を置いてやり直してください。'
        }
      }
    },
    async getReginData() {
      const regionData = await this.$api.getRegion(`city_code=${this.citycode}`)
      // console.log(regionData)
      if (regionData.status == 200) {
        this.baseColor = regionData.data.base_color
        this.$nuxt.$emit('updateLayout', regionData.data)
      } else {
        if (regionData.data) {
          errorMessage = region.data.detail
        } else {
          errorMessage = 'サーバーエラーです、時間置いてからお試しください'
        }
      }
    },
  },
  created() {
    this.activate()
    this.getReginData()
  },
}
</script>