<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <ReservationFacilityInfo2
            :facilityItem="facilityData"
          />
          <ReservationConfirmCard
            v-if="Object.keys(facilityData).length !== 0"
            :citycode="regionData.city_code"
            :baseColor="regionData.base_color"
            :facilityId="facilityData.id"
            :temporaryReservationId="this.temporaryReservationId"
            :questions="this.questions"
            @stopCancelingReservationTmp="stopCancelingReservationTmp"
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
      temporaryReservationId: [],
      questions: [],
      isReservationTmpCancel: true,
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
  async created () {
    if (!this.$auth.loggedIn) {
      this.$router.push(`/account?citycode=${this.$route.query.citycode}`)
      return
    }

    // 仮予約
    const payload = {
      'email': this.$auth.user.email,
      'slotId': this.$route.query.slotId.split(',')
    }
    const response = await this.$api.postReservationTmp(payload)
    const data = Array.isArray(response.data) ? response.data : [response.data];
    if (response.status == 201) {
      this.temporaryReservationId = data.map((item)=>item.id)
      if ('questions' in data[0]['survey']) {
        this.questions = data[0]['survey']['questions']
      }
    }else{
      return this.$notifier.showMessage({ content: '仮予約に失敗しました。', color: 'error' })
    }
  },
  async destroyed () {
    if (this.isReservationTmpCancel && this.temporaryReservationId) {
      const payload = {
        'email': this.$auth.user.email
      }

      // 仮予約キャンセル
      const reservationTmp = await this.$api.cancelReservationTmp(`reservationTemporaryId=${this.temporaryReservationId.join(',')}`, payload)
    }
  },
  async fetch({ route, store }) {
    store.dispatch('facility/getFacilityData', { facilityId: route.query.facilityId, citycode: route.query.citycode })
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
      facilityData: 'facility/getFacility',
    }),
  },
  methods: {
    stopCancelingReservationTmp() {
      this.isReservationTmpCancel = false
    }
  },
}
</script>
