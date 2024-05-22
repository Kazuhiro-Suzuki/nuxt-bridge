<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" :md="cardCols" :lg="cardCols" :xl="cardCols">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <ReservationFacilityInfo2
            :facilityItem="facilityData"
          />
          <v-card-actions class="justify-center">
            <SlotCard
              :regionItem="regionData"
              :facilityItem="facilityData"
              :slotItems="slotData"
            />
          </v-card-actions>
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
    return  {
      title: '短期入所施設 予約',
      citycode: this.$route.query.citycode,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
      facilityData: 'facility/getFacility',
      slotData: 'slot/getSlot',
    }),
    cardCols(){
      if (this.citycode == '142077') {
        return 10
      }
      return 8
    }
  },
  async asyncData({ route, $api }){
    let title = ""
    const reservationConnectResponse = await $api.getReservationConnection(`city_code=${route.query.citycode}`)
    if (reservationConnectResponse.status == 200) {
      title = reservationConnectResponse.data.title + ' 予約'
    } 
    return {
      title
    }
  },
  async fetch({ route, store }) {
    store.dispatch('facility/getFacilityData', { facilityId: route.query.facilityId, citycode: route.query.citycode })
    store.dispatch('slot/getSlotData', { facilityId: route.query.facilityId, citycode: route.query.citycode })
  },
}
</script>
