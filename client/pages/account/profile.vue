<template>
  <v-container>
    <v-row justify="center" align="center" class="my-10">
      <v-col sm="8" md="7" lg="7" xl="7">
        <!-- <ProfileCard
          v-if="!($auth.loggedIn && $auth.user.type === 'facility')"
          :title="title"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :citycode="regionData.city_code"
          :userInfo="userInfo"
        /> -->
        <component
          :is="profileCardComponent"
          v-if="!($auth.loggedIn && $auth.user.type === 'facility')"
          :title="title"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :citycode="regionData.city_code"
          :userInfo="userInfo"
        />
        <FacilityUserProfileCard
          v-else
          :title="title"
          :baseColor="regionData.base_color"
          :citycode="regionData.city_code"
          :userInfo="userInfo"
        />
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col sm="8" md="7" lg="7" xl="7">
        <AccountDeleteCard
          title="退会"
          :citycode="regionData.city_code"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :userInfo="userInfo"
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
      title: 'プロフィール'
    }
  },
  data() {
    return {
      title: 'プロフィール',
      userInfo: {},
      errorMessage: '',
    }
  },
  async asyncData({ app, $api, $auth, route }) {
    if (!$auth.loggedIn) {
      await app.router.push({
            path: '/account',
            query: {
              citycode: route.query.citycode,
              redirect_uri: encodeURIComponent(`/account/profile?citycode=${route.query.citycode}`),
            }
          })
      return;
    }
    let errorMessage = ''
    let userInfo = {}
    const response = await $api.getUserInfo()
    if (response.status = 200) {
      userInfo = response.data
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = ''
      }
    }
    return {
      userInfo,
      errorMessage,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    profileCardComponent(){
      return () => import(`@/components/organisms/account/region/${this.regionData.city_code}/ProfileCard.vue`) 
    }
  },
}
</script>