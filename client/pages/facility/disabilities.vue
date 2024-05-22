<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <v-card-text>
            <v-row justify="center">
              <v-col cols="12" v-for="category in facilityCategories"
                :key="category.id">
                <v-card v-if="category.facilityItems && category.facilityItems.length">
                  <v-card class="elevation-0 lighten-4 font-weight" :color='regionData.base_color'>
                    <v-card-title>{{ category.name }}</v-card-title>
                    <v-card-text v-if="category.contents">{{ category.contents }}</v-card-text>
                  </v-card>
                  <v-card-text>
                    <v-row justify="center">
                      <v-col>
                        <DisabledFacilityList
                          :facilityItems="category.facilityItems"
                          :baseColor="regionData.base_color"
                          :citycode="citycode"
                        />
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
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
      title: '障害者施設 一覧',
      citycode: this.$route.query.citycode
    }
  },
  async asyncData({ route, $api }) {
    let facilityCategories = []
    let errorMessage = ''
    const response = await $api.getPublicFacilities(`city_code=${route.query.citycode}&facility_type=disabled_facility`)
    if (response.status === 200) {
      facilityCategories = response.data
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
    return {
      facilityCategories,
      errorMessage,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
}
</script>
