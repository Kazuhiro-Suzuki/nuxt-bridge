<template>
  <v-container>
    <v-row justify="center" v-if="!isMaintenance">
      <v-col xs="12" sm="10" md="8" lg="8" xl="8">
        <HistoryCard
          :title="title"
          :baseColor="regionData.base_color"
          :reservations="reservationData"
          :slotData="slotData"
          :facilityData="facilityData"
        />
      </v-col>
    </v-row>
    <v-row justify="center" v-else>
      <v-col xs="12" sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <v-card-text>
            <p class="text-h6" style="color:red">只今、{{ title }}の予約履歴はメンテナンス中です。今しばらくお待ちください。</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  meta: {
    back: true
  },
  middleware: 'authenticated',
  head() {
    return {
      title: this.title
    }
  },
  mounted() {
    if (this.errorMessage) {
      this.$notifier.showMessage({ content: this.errorMessage, color: 'error'})
    }
  },
  async asyncData({ route, $api }) {
    let reservationData = []
    let facilityData = {}
    let slotData = {}
    let isMaintenance = false
    let title = ""
    const reservationConnectResponse = await $api.getReservationConnection(`city_code=${route.query.citycode}`)
    if (reservationConnectResponse.status == 200) {
      title = reservationConnectResponse.data.title + " 予約履歴"
      isMaintenance = !reservationConnectResponse.data.is_active;
    } else {
        return {
          title: "",
          reservationData: [],
          facilityData: {},
          slotData: {},
          isMaintenance: isMaintenance,
          errorMessage: 'サーバーエラーです、時間置いてからお試しください。',
        }
    }

    const userInfoResponse = await $api.getUserInfo()
    if (userInfoResponse.status !== 200) {
      return {
        title: title,
        reservationData: [],
        facilityData: {},
        slotData: {},
        isMaintenance: isMaintenance,
        errorMessage: '施設予約履歴情報が取得できませんでした。',
      }
    }
    const reservationResponse = await $api.getReservation(`uid=${userInfoResponse.data['uid']}`)
    if (reservationResponse.status !== 200) {
      return {
        title: title,
        reservationData: [],
        facilityData: {},
        slotData: {},
        isMaintenance: isMaintenance,
        errorMessage: '施設予約履歴情報が取得できませんでした。',
      }
    }
    if (reservationResponse.status !== 200) {
      return {
        title: title,
        reservationData: [],
        facilityData: {},
        slotData: {},
        isMaintenance: isMaintenance,
        errorMessage: '施設予約履歴情報が取得できませんでした。',
      }
    }
    reservationResponse.data.reverse().forEach(reservation => {
      reservationData.push(reservation)
    })

    const facilityResponse = await $api.getReservationFacility( `city_code=${route.query.citycode}` )
    if (facilityResponse.status !== 200) {
      return {
        title: title,
        reservationData: [],
        facilityData: {},
        slotData: {},
        isMaintenance: isMaintenance,
        errorMessage: '施設予約履歴情報が取得できませんでした。',
      }
    }
    facilityResponse.data.forEach(facility => {
      facilityData[facility.id] = {
        address: facility.address,
        displayName: facility.displayName,
        phoneNumber: facility.phoneNumber,
      }
    })

    const response = await $api.postSlot({ citycode: route.query.citycode, range: true })
    if (response.status !== 200) {
      return {
        title: title,
        reservationData: [],
        facilityData: {},
        slotData: {},
        isMaintenance: isMaintenance,
        errorMessage: '施設予約履歴情報が取得できませんでした。',
      }
    }
    response.data.forEach((slot) => {
      slotData[slot.id] = {
        date: slot.date,
        division: slot.division,
        facilityId: slot.facilityId,
        openAt: slot.openAt,
        closeAt: slot.closeAt
      }
    })
    return {
      title: title,
      reservationData,
      facilityData,
      slotData,
      isMaintenance,
      errorMessage: '',
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  }
}
</script>
