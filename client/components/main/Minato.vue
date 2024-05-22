<template>
  <v-container>
    <v-row justify="center">
      <v-col v-if="topImage" xs="12" sm="10" md="8" lg="8" xl="8">
        <v-card class="text--center" elevation="5">
          <v-img :src="'/specific/' + topImage" class="white--text align-end"></v-img>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col xs="12" sm="10" md="8" lg="8" xl="8">
        <NotificationCard
          :citycode="citycode"
          :item="item"
        />
      </v-col>
      <v-col xs="12" sm="10" md="8" lg="8" xl="8"
        v-for="(item, i) in buttons"
        :key=i
        cols="12"
      >
        <MainMenuButton
          :i="i"
          :to="item.to"
          :imgFile="item.imgFile"
          :title="item.title"
          :type="item.type"
        />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col xs="12" sm="10" md="8" lg="8" xl="8" class="text-center">
         <NuxtLink :to="{ path: 'account/profile', query: { citycode: this.citycode }}" class="nuxt-profile-link">
          配信停止もしくは退会処理を希望する方はこちら
        </NuxtLink>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col class="d-flex justify-end">
        <a
          href="https://play.google.com/store/apps/details?id=com.lg_pwd_native"
          target="_blank"
        >
          <v-img
            src="common/android.png"
            :max-height="maxHeight"
            :max-width="maxWidth"
          >
          </v-img>
        </a>
      </v-col>
      <v-col class="d-flex justify-start">
        <a
          href="https://apps.apple.com/app/apple-store/id1583696042?mt=8"
          target="_blank"
        >
          <v-img
            src="common/ios.png"
            :max-height="maxHeight"
            :max-width="maxWidth"
          >
          </v-img>
        </a>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { homeButton } from '../../model/homeButton'

export default {
  head() {
    return {
      title: 'ホーム',
    }
  },
  props: {
    item: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      citycode: this.$route.query.citycode,
      fullPath: this.$route.fullPath,
      maxHeight: 50,
      maxWidth: 140,
      buttons: [],
    }
  },
  computed: {
    topImage() {
      return this.$store.state.region?.regionData?.top_image
    }
  },
  created(){
    let buttonInfo = homeButton.find(item => item.city_code ==  this.citycode);
    this.buttons = buttonInfo.mainButtons
  }
}
</script>

<style scoped>
 .nuxt-profile-link {
   color: black;
 }
</style>