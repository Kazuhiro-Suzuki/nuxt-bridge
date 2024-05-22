<template>
  <v-container>
    <v-row justify="center" align="center" style="height: 600px;">
      <v-col sm="8" md="6" lg="6" align="center">
        <LoginForm
          :title="title"
          :baseColor="regionData.base_color"
          :citycode="citycode"
          :fullPath="fullPath"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  head() {
    return {
      title: 'ログイン'
    }
  },
  data() {
    return {
      title: 'ログイン',
      citycode: this.$route.query.citycode,
      fullPath: this.$route.fullPath
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
}
</script>
