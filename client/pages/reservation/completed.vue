<template>
  <v-container>
    <v-row justify="center">
      <v-col xs="12" sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <ReservationFacilityInfo2
            :facilityItem="facilityData"
          />
          <ReservationCompleteCard
            :reservationData="reservationData"
            :slotData="slotData"
            :facilityData="facilityData"
            :citycode="$route.query.citycode"
          />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  head() {
    return {
      title: this.title
    }
  },
  data() {
    return {
      title: '短期入所施設 予約',
      reservation: {}
    }
  },
  async created () {
    if (!this.$auth.loggedIn) {
      this.$router.push(`/account?citycode=${this.$route.query.city_code}`)
    }
  },
  mounted() {
    if (this.errorMessage) {
      this.$notifier.showMessage({ content: this.errorMessage, color: 'error' })
    }
  },
  async asyncData({ route, $api, $auth }) {
    let title = ""
    const reservationConnectResponse = await $api.getReservationConnection(`city_code=${route.query.citycode}`)
    if (reservationConnectResponse.status == 200) {
      title = reservationConnectResponse.data.title + ' 予約'
    } 

    const userInfoResponse = await $api.getUserInfo()
    if (userInfoResponse.status !== 200) {
      return {
        title: title,
        reservationData: {},
        facilityData: {},
        slotData: {},
        errorMessage: '予約情報が取得できませんでした。',
      }
    }
    const reservationResponse = await $api.getReservation(`uid=${userInfoResponse.data['uid']}&reservationId=${route.query.reservationId}`)
    if (reservationResponse.status !== 200) {
      return {
        title: title,
        reservationData: {},
        facilityData: {},
        slotData: {},
        errorMessage: '予約情報が取得できませんでした。',
      }
    }
    const reservationData = reservationResponse.data
    const slotIds = [];
    for(const eachReservationData of reservationData){
      slotIds.push(eachReservationData['slotId'])
    }
    const slotResponse = await $api.getSlot(`city_code=${route.query.citycode}&slotId=${slotIds.join(',')}`)
    if (slotResponse.status !== 200) {
      return {
        title: title,
        reservationData: {},
        facilityData: {},
        slotData: {},
        errorMessage: '予約情報が取得できませんでした。',
      }
    }
    const slotData = Array.isArray(slotResponse.data) ? slotResponse.data : [slotResponse.data]

    const facilityResponse = await $api.getReservationFacilityDetail(`city_code=${route.query.citycode}&facilityId=${slotData[0]['facilityId']}`);
    if (facilityResponse.status !== 200) {
      return {
        title: title,
        reservationData: {},
        facilityData: {},
        slotData: {},
        errorMessage: '予約情報が取得できませんでした。',
      }
    }
    const facilityData = facilityResponse.data

    return  {
      title: title,
      reservationData,
      slotData,
      facilityData,
      errorMessage: '',
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    })
  }
}
</script>
