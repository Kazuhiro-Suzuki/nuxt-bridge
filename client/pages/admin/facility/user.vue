<template>
  <v-container>
    <v-row>
      <v-col>
        <ErrorAlert :message="errorMessage" />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col xs="12" sm="12" md="8" lg="8" xl="8">
        <NewFacilityUserPost
          :citycode="citycode"
          :items="facilityItems"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <FacilityUserTable
          :title="title"
          :items="items"
          :facilityItems="facilityItems"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
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
      title: '施設ユーザー管理',
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
    const response = await $api.getFacilityUserList(`city_code=${route.query.citycode}`)
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

    let facilityItems = []
    const facilityResponse = await $api.getAllPublicFacilities(`city_code=${route.query.citycode}`)
    // console.log(response)
    if (facilityResponse.status == 200) {
      facilityItems = facilityResponse.data
    } else{
      if (facilityResponse.data.detail) {
        errorMessage = facilityResponse.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
    return {
      items,
      facilityItems,
      errorMessage,
    }
  }
}
</script>