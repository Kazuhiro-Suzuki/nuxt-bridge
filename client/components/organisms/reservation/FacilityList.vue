<template>
  <v-row>
    <v-col
      cols="12"
      v-for="(item, i) in facilityItems"
      :key=i
    >
      <v-card>
        <ReservationFacilityInfo2
          :facilityItem="item"
        />
        <v-card-actions>
          <v-spacer></v-spacer>
          <NormalButton
            text="詳 細"
            color="grey lighten-2"
            @clickAction="$router.push(`/reservation/detail?citycode=${item.cityCode}&facilityId=${item.id}`)"
          />
          <NormalButton
            text="予 約"
            :color="`${baseColor} lighten-4`"
            :disabled="(!$auth.loggedIn || $auth.user.type !== 'general')"
            @clickAction="$router.push(`/reservation/list?citycode=${item.cityCode}&facilityId=${item.id}`)"
          />
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    facilityItems: {
      type: Array,
      required: true
    },
    baseColor: {
      type: String,
      required: true
    },
  }
}
</script>
