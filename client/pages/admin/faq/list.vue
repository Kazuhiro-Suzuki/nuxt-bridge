<template>
  <v-container>
    <v-row>
      <v-col>
        <ErrorAlert :message="errorMessage" />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col xs="12" sm="12" md="8" lg="8" xl="8">
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <AdminInquiryList
          :title="title"
          :items="items"
          :citycode="citycode"
          :baseColor="regionData.base_color"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  head() {
    return {
      title: this.title,
    }
  },
  data() {
    return {
      title: 'お問い合わせ管理',
      citycode: this.$route.query.citycode,
      items: [],
      errorMessage: '',
    }
  },
  computed: {
    ...mapState({
      regionData: state => state.region.regionData
    })
  },
  async asyncData({ route, $api }) {
    let items = []
    let errorMessage = ''
    const response = await $api.getAdminInquiryList(`city_code=${route.query.citycode}`)
    // console.log(response)
    if (response.status == 200) {
      items = response.data
    } else{
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
    return {
      items,
      errorMessage,
    }
  }
}
</script>