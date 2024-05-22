<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <FacilityDetailCard
            :cityCode="regionData.city_code"
            :baseColor="regionData.base_color"
            :facilityItem="facilityData"
          />
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
      title: '短期入所施設 予約',
      baseColor: '',
      citycode: this.$route.query.citycode
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
      facilityData: 'facility/getFacility',
    })
  },
  async async(){
    let title = ""
    const reservationConnectResponse = await $api.getReservationConnection(`city_code=${route.query.citycode}`)
    if (reservationConnectResponse.status == 200) {
      title = reservationConnectResponse.data.title + " 予約履歴"
    } 
    console.log(this.title);
    return {
      title
    }
  },
  async fetch({ route, store }) {
    store.dispatch('facility/getFacilityData', { facilityId: route.query.facilityId, citycode: route.query.citycode })
  },
}
</script>
