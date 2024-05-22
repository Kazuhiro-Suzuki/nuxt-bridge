<template>
  <v-card elevation="0">
    <v-card-title class="text-h6">
      {{ facilityItem.displayName }}
    </v-card-title>
    <v-card-text>
      <div class="font-weight-bold">住所</div>
      <div class="px-1">{{ facilityItem.address }}</div>
      <div class="font-weight-bold">電話</div>
      <div class="px-1">{{ facilityItem.phoneNumber }}</div>
      <div class="font-weight-bold" v-if="facilityItem.tags[0]">対象者</div>
      <div class="px-1">{{ facilityItem.tags[0] }}</div>
      <div class="font-weight-bold" v-if="facilityItem.tags[1]">予約について</div>
      <div class="px-1" style="white-space: pre-wrap;">{{ reserveDescription(facilityItem.tags[1]) }}</div>
      <div class="font-weight-bold" v-if="facilityItem.tags[2]">連続利用期間</div>
      <div class="px-1">{{ facilityItem.tags[2] }}</div>
      <div class="font-weight-bold" v-if="facilityItem.tags[3]">その他</div>
      <div class="px-1">{{ facilityItem.tags[3] }}</div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    facilityItem: {
      type: Object,
      required: true
    },
  },
  methods: {
    reserveDescription(facilityItem){
      if(facilityItem){
        let i = 0;
        return facilityItem.replace(/・/g, m  => !i++ ? m : '\n・');
      }
    }
  }
}
</script>