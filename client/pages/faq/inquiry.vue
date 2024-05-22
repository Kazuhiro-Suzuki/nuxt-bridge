<template>
  <v-container>
    <v-row justify="center"  v-if="(!$auth.loggedIn || $auth.user.type == 'business') || citycode == '131237'">
      <v-col sm="10" md="8" lg="8" xl="8">
        <ContactInfoCard />
      </v-col>
    </v-row>
    <div v-else>
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
      <v-row justify="center">
        <v-col cols="12">
          <v-card>
            <DenseToolBar
              :baseColor="regionData.base_color"
              :title="title"
            />
            <v-card-text class="text-center" v-if="!inquiryItems.length">
              データがありません
            </v-card-text>
            <v-card-text v-else>
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
    </div>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  meta: {
    back: true
  },
  head() {
    return {
      title: this.title,
    }
  },
  data() {
    return {
      title: 'お問い合わせ',
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
    const response = await $api.getUserInquiryList(`city_code=${route.query.citycode}`)
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