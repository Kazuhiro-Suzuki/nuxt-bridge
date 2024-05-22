<template>
  <v-container>
    <v-overlay v-if="showLoading" style="z-index: 206">
          <h2>読み込み中</h2>
    </v-overlay>
    <v-row>
      <v-col>
        <ErrorAlert :message="errorMessage" />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col xs="12" sm="12" md="8" lg="8" xl="8">
        <NewFacilityPost
          :citycode="citycode"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          @showLoading="showLoading = !showLoading"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <FacilityTable
          :title="title"
          :items="items"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          @showLoading="showLoading = !showLoading"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  middleware: ['authenticated'],
  head() {
    return {
      title: '施設情報管理',
    }
  },
  data() {
    return {
      title: '施設情報管理',
      citycode: this.$route.query.citycode,
      items: [],
      errorMessage: '',
      showLoading: false
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
    const response = await $api.getAllPublicFacilities(`city_code=${route.query.citycode}`)
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