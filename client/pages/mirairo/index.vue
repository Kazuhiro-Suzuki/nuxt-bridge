<template>
  <v-container>
    <v-row class="py-6">
      <v-col cols="12">
        <mirairo-title />
      </v-col>
    </v-row>
    <v-row v-if="!isActive" justify="center">
      <v-col xs="12" sm="10" md="8" lg="8" xl="8">
        <!-- <mirairo-closed-card
          :citycode="citycode"
          :baseColor="regionData.base_color"
        /> -->
        <mirairo-info-card
          :citycode="citycode"
          :baseColor="regionData.base_color"
        />
      </v-col>
    </v-row>
    <v-row v-else-if="loggedIn" justify="center">
      <v-col xs="12" sm="10" md="8" lg="8" xl="8">
        <mirairo-connect-card
          :citycode="citycode"
          :profile="regionProfile"
          :user-connection="userConnection"
          :baseColor="regionData.base_color"
          @disconnect="onDisconnectClicked"
        />
      </v-col>
    </v-row>
    <v-row v-else justify="center">
      <v-col xs="12" sm="10" md="8" lg="8" xl="8">
        <mirairo-intro-card
          :citycode="citycode"
          :baseColor="regionData.base_color"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import MirairoConnectCard from "../../components/organisms/mirairo/MirairoConnectCard";
import MirairoIntroCard from "../../components/organisms/mirairo/MirairoIntroCard";
import MirairoClosedCard from "../../components/organisms/mirairo/MirairoClosedCard";
import MirairoTitle from "../../components/organisms/mirairo/MirairoTitle";

export default {
  components: {MirairoConnectCard, MirairoIntroCard, MirairoClosedCard, MirairoTitle},
  head() {
    return {
      title: 'ミライロID連携'
    }
  },
  data() {
    return {
      citycode: this.$route.query.citycode,
      title: 'ミライロID連携',
    }
  },
  async asyncData({ route, $api, $auth, app, }) {
    const isMobileOrTablet = app.context.$device.isMobileOrTablet
    if (isMobileOrTablet && app.context.from.name == 'mirairo' && !$auth.loggedIn) {
      let data = {
        'from_path': app.context.from.name,
        'email': route.query.email,
        'city_code': route.query.citycode,
      }
      $auth.loginWith('refresh', { data: data })
        .then(() => {
          app.router.push(`/mirairo/bastion?citycode=${route.query.citycode}`)
        })
    }

    const res = await $api.getMirairoConnectInitialData(route.query.citycode)
    return {
      loggedIn: $auth.loggedIn,
      regionProfile: res.data.regionProfile,
      userConnection: res.data.userConnection
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    isActive() {
      if (!this.regionProfile) return false;
      return this.regionProfile.isActive
    }
  },
  methods: {
    onDisconnectClicked() {
      this.$router.push({
        path: '/mirairo/disconnect',
        query: this.$route.query
      })
    }
  }
}
</script>
