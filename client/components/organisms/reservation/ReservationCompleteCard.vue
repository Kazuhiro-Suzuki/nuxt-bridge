<template>
  <div>
    <v-card-text>
      <v-row justify="center">
        <v-col cols="12" v-for="eachSlotData in slotData" :key="eachSlotData.id">
          予約枠：{{ eachSlotData['date'] }} {{ eachSlotData['division'] }}
        </v-col>
        <v-col cols="12">
          予約が完了しました。<br/>
          会員登録の際にいただいたメールアドレスに自動送信でメールをお送りいたします。
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <NormalButton
        color="grey lighten-3"
        text="TOPページに戻る"
        :block="buttonBlock"
        @clickAction="$router.push(`/home?citycode=${citycode}`)"
      />
    </v-card-actions>
  </div>
</template>

<script>
export default {
  props: {
    reservationData: {
      type: Array,
      required: true,
    },
    slotData: {
      type: Array,
      required: true,
    },
    facilityData: {
      type: Object,
      required: true,
    },
    citycode: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      buttonBlock: true,
    }
  }
}
</script>
