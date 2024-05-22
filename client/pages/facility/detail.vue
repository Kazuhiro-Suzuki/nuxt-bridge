<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <v-card-text>
            <v-row justify="center">
              <v-col>
                <DisabledFacilityDetail
                  :baseColor="regionData.base_color"
                  :cityCode="citycode"
                  :facilityItem="facilityItems"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  head() {
    return {
      title: this.title
    }
  },
  data() {
    return {
      title: '詳細',
      baseColor: '',
      citycode: this.$route.query.citycode,
      facilityId: this.$route.query.facilityId
    }
  },
  async asyncData({ route, $api }) {
    let facilityItems = []
    let errorMessage = ''
    const response = await $api.getPublicFacilities(`facility_id=${route.query.facilityId}`)
    if (response.status === 200) {
      facilityItems = response.data
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
    return {
      facilityItems,
      errorMessage,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
}
</script>
