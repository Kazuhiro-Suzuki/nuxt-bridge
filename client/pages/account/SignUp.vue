<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="8" md="6" lg="6" xl="6" align="center">
        <ErrorAlert :message="errorMessage" />
      </v-col>
    </v-row>
    <v-row justify="center" align="center" style="height: 100%;">
      <v-col sm="8" md="7" lg="7" xl="7" align="center">
        <!-- <SignUpForm
          :title="title"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :citycode="citycode"
          :fullPath="fullPath"
          @errorEvent="errorMessage = $event"
        /> -->
        <component 
          :is="signUpFormComponent" 
          :title="title"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :citycode="citycode"
          :fullPath="fullPath"
          @errorEvent="errorMessage = $event"
        />
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
      title: '会員登録',
    }
  },
  data() {
    return {
      title: '会員登録',
      citycode: this.$route.query.citycode,
      fullPath: this.$route.fullPath,
      errorMessage: '',
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    signUpFormComponent(){
      return () => import(`@/components/organisms/account/region/${this.regionData.city_code}/SignUpForm.vue`) 
    }
  },
}
</script>