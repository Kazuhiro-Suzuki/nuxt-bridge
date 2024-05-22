<template>
  <v-container class="font-style">
    <v-row justify="center" class="pb-2">
      <v-col v-if="topImage" xs="12" sm="12" md="11" lg="11" xl="11">
        <v-card class="text--center" elevation="5">
          <v-img :src="'/specific/' + topImage" :max-height="imgMaxHeight" class="white--text align-end"></v-img>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-md-3">
      <v-col xs="12" sm="12" md="11" lg="11" xl="11">
        <!-- <NotificationSimpleCard
          baseColor="white"
          darkColor="white"
          :citycode="citycode"
          :item="item"
          :icon="'$IconInformation2tDarkGreen'"
        /> -->
        <NotificationSimpleText
          :citycode="citycode"
          :item="item"
          :icon="'$IconInformation2tDarkGreen'"
        />
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-3">
      <v-col xs="12" sm="12" md="11" lg="11" xl="11">
        <v-row justify="center">
          <v-col md="6" lg="6" xl="6"
            v-for="(item, i) in mainButtons"
            :key=i
            cols="12"
          >
            <HomeMainMenuButton
              :i="i"
              :to="item.to"
              :imgFile="item.imgFile"
              :icon="item.icon"
              :size="$vuetify.breakpoint.mobile ? '30px': '50px'"
              :height="$vuetify.breakpoint.mobile ? '100': '150'"
              :title="item.title"
              :type="item.type"
              buttonRounded="rounded-lg"
              buttonAlign="horizontal-align"
              :buttonPadding="$vuetify.breakpoint.mobile ? 'py-5 px-2' :'py-11 px-5'"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-3">
      <v-col xs="12" sm="12" md="11" lg="11" xl="11">
        <v-row justify="center" :dense="$vuetify.breakpoint.mobile">
          <v-col
            v-for="(item, i) in subButtons"
            :key=i
            cols="4"
          >
            <HomeMainMenuButton
              :i="i"
              :to="item.to"
              :imgFile="item.imgFile"
              :icon="item.icon"
              :size="$vuetify.breakpoint.mobile ? '40px': '70px'"
              :height="$vuetify.breakpoint.mobile ? '100': '150'"
              :title="item.title"
              :type="item.type"
              :baseColor="regionData.base_color"
              buttonRounded="rounded-lg"
              buttonAlign="vertical-align"
              :buttonPadding="$vuetify.breakpoint.mobile ? 'py-4 px-1':'py-10'"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="!$auth.loggedIn">
      <v-col xs="12" sm="12" md="11" lg="11" xl="11">
        <LoginCardOneRow
          baseColor="white--text"
          darkColor="white"
          btnClass="rounded-lg font-weight-bold"
          :width="$vuetify.breakpoint.mobile ? '90%' : '80%'"
          :buttonTextColor="regionData.dark_color"
          :citycode="citycode"
        />
      </v-col>
    </v-row>
    <div style="padding-top: 100px;" v-if="!$vuetify.breakpoint.mobile">
      <v-row justify="center" class="pb-10">
          <div class="font-weight-bold">
            アプリのダウンロードはこちらから
          </div>
      </v-row>
      <v-row dense>
        <v-col class="d-flex justify-end">
          <a
            href="https://play.google.com/store/apps/details?id=com.lg_pwd.hida"
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
            href="https://apps.apple.com/app/apple-store/id6472247681?mt=8"
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
    </div>
  </v-container>
</template>

<script>
import { homeButton } from '@/model/homeButton'
import { mapGetters } from 'vuex'
 
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
      maxHeight: 60,
      maxWidth: 150,
      imgMaxHeight: 600,
      mainButtons: [],
      subButtons: []
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    topImage() {
      return this.$store.state.region?.regionData?.top_image
    },
    adStyle(){
      if(this.$vuetify.breakpoint.mobile){
        return 'breaking-mobile-out'
      }
      return 'breaking-out'
    }
  },
  created(){
    let buttonInfo = homeButton.find(item => item.city_code ==  this.citycode);
    this.mainButtons = buttonInfo.mainButtons
    this.subButtons = buttonInfo.subButtons
  }
}
</script>

<style scoped>
 .nuxt-profile-link {
   color: black;
 }
</style>

<style>
 .font-style {
  font-family: 'Hiragino Kaku Gothic'
 }

.breaking-mobile-out {
	margin-right: calc(50% - 50vw);
	margin-left: calc(50% - 50vw);
  overflow: hidden;
  background: #F5F5F5; 
}
.breaking-out {
	margin-right: calc(50% - 50vw);
	margin-left: calc(50% - 50vw);
  overflow: hidden;
  background: #F5F5F5; 
}
</style>