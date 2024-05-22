<template>
  <v-container>
    <v-row justify="center" align="center" style="height: 600px;">
      <v-col sm="8" md="6" lg="6" align="center">
        <ConfirmEmailForm
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
import { mapState } from 'vuex'

export default {
  meta: {
    back: true
  },
  head() {
    return {
      title: 'メールアドレス確認'
    }
  },
  data() {
    return {
      title: 'メールアドレス確認',
      citycode: this.$route.query.citycode,
      fullPath: this.$route.fullPath
    }
  },
  computed: {
    ...mapState({
      regionData: state => state.region.regionData
    })
  }
}
</script>
