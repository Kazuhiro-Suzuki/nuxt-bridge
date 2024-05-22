<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="baseColor"
            :title="title"
          />
          <v-card-text v-if="!isMaintenance">
            <v-list-item
                class="pl-0 pr-0"
                v-for="(item, i) in items"
                :key="i"
              >
                <v-list-item-avatar class="mt-0 mb-0 mr-0">
                  <v-icon>mdi-circle-small</v-icon>
                </v-list-item-avatar>
                <v-list-item-content class="subtitle-1">
                  {{ item.text }}
                </v-list-item-content>
              </v-list-item>
            <FacilityList
              :facilityItems="facilityItems"
              :baseColor="baseColor"
            />
          </v-card-text>
          <v-card-text v-else>
            <p class="text-h6" style="color:red">只今、{{ title }}はメンテナンス中です。今しばらくお待ちください。</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
export default {
  props: {
    baseColor: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    facilityItems: {
      type: Array,
      required: true,
    },
    items: {
      type: Array,
      required: true,
    },
    isMaintenance: {
      type: Boolean,
      required: true,
    },
  },
}
</script>
