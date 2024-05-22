<template>
<v-row>
    <v-col
      cols="12"
      v-for="(item, i) in facilityItems"
      :key=i
    >
      <v-card>
        <v-card-title class="text-h6" style="white-space: pre-line">{{ item.name }}</v-card-title>
        <v-card-subtitle>
          {{ item.business_description }}
        </v-card-subtitle>
        <v-card-text>
          <div class="font-weight-bold">電話</div>
          <div class="px-1">{{ item.phone_number }}</div>
          <div class="font-weight-bold">FAX</div>
          <div class="px-1">{{ item.fax_number }}</div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <NormalButton
            text="詳 細"
            color="grey lighten-2"
            @clickAction="$router.push(`/facility/detail?citycode=${citycode}&facilityId=${item.id}`)"
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
    citycode: {
      type: String,
      required: true
    }
  }
}
</script>
