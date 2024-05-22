<template>
  <div>
    <v-card>
      <ReservationFacilityInfo2
        :facilityItem="facilityItem"
      />
      <v-card-actions>
        <v-row justify="center">
          <v-col cols="4">
            <NormalButton color="grey lighten-2" text="HP" @clickAction="homePage" :block="block" />
          </v-col>
          <v-col cols="4">
            <NormalButton color="grey lighten-2" text="地図" @clickAction="map" :block="block" />
          </v-col>
          <v-col cols="4">
            <NormalButton color="grey lighten-2" text="電話" @clickAction="tel" :block="block" />
          </v-col>
        </v-row>
      </v-card-actions>
      <v-card-actions>
        <v-spacer></v-spacer>
        <NormalButton
          color="grey lighten-2"
          text="戻 る"
          @clickAction="$router.push(`/reservation?citycode=${cityCode}`)"
        />
        <NormalButton
          :color="`${baseColor} lighten-4`"
          text="予 約"
          :disabled="(!$auth.loggedIn || $auth.user.type !== 'general')"
          @clickAction="$router.push(`/reservation/list?citycode=${cityCode}&facilityId=${facilityItem.id}`)"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    baseColor: {
      type: String,
      required: true
    },
    cityCode: {
      type: String,
      required: true
    },
    facilityItem: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      block: true
    }
  },
  methods: {
    tel() {
      window.location.href = `tel:${this.facilityItem.phoneNumber}`
    },
    homePage() {
      window.open(this.facilityItem.homepage, '_blank')
    },
    map() {
      window.open(this.facilityItem.mapUrl, '_blank')
    },
  },
}
</script>
