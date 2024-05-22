<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <v-card elevation="0">
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <v-card-text>
            <TermOfServiceText 
              :text="regionData.term_of_service"
            />
          </v-card-text>
          <v-card-actions class="justify-center">
            <NormalButton
              text="同意して会員登録に進む"
              :class="`${regionData.base_color} lighten-4`"
              :color="regionData.base_color"
              @clickAction="$router.push(`/account/signup?citycode=${citycode}`)"
            />
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  meta: {
    back: true
  },
  head() {
    return {
      title: '利用規約'
    }
  },
  data() {
    return {
      title: '利用規約',
      citycode: this.$route.query.citycode,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
}
</script>