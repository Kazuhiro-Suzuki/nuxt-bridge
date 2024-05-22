<template>
  <v-container>
    <v-row justify="center">
        <v-col xs="12" sm="12" md="8" lg="8" xl="8">
            <NewInquiryPost
            :citycode="citycode"
            :baseColor="regionData.base_color"
            :darkColor="regionData.dark_color"
            :bodyMaxLength="bodyMaxLength"
            />
        </v-col>
    </v-row>
    <v-row class="d-flex justify-space-around">
      <v-col>
          <v-card>
            <DenseToolBar
                :baseColor="regionData.base_color"
                :title="title"
            />
            <v-card-text>
                <v-row justify="center">
                  <v-col>
                      <InquiryList
                              :inquiryItems="inquiryItems"
                              :baseColor="regionData.base_color"
                              :citycode="citycode"
                              />
                  </v-col>
                </v-row>
            </v-card-text>
          </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  middleware: ['authenticated'],
  head() {
    return {
      title: this.title,
    }
  },
  data() {
    return {
      title: 'お問い合わせ履歴',
      citycode: this.$route.query.citycode,
      bodyMaxLength: '2000',
      errorMessage: ''
    }
  },
  computed: {
    ...mapState({
      regionData: state => state.region.regionData
    })
  },
  async asyncData({ route, $api }) {
    let inquiryItems = []
    let errorMessage = ''
    const response = await $api.getAdminInquiryDetail(route.params.userId, `city_code=${route.query.citycode}`)
    if (response.status === 200) {
      inquiryItems = response.data
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
    return {
      inquiryItems,
      errorMessage,
    }
  },
}
</script>