<template>
  <v-container>
    <v-row justify="center" align="center" style="height: 600px;">
      <v-col sm="8" md="12" lg="6" xl="6">
        <ResetPasswordForm
          :title="title"
          :citycode="citycode"
          :uid="uid"
          :baseColor="regionData.base_color"
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
      title: 'パスワードリセット'
    }
  },
  data() {
    return {
      title: 'パスワードリセット',
      citycode: this.$route.query.citycode,
      uid: this.$route.query.uid,
      baseColor: '',
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  }
}
</script>
