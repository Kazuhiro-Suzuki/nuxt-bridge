<template>
  <v-container class="font-style">
    <v-row justify="center" class="pb-2">
      <v-col v-if="topImage" xs="12" sm="12" md="11" lg="11" xl="11">
        <v-card class="text--center" elevation="5">
          <v-img :src="'/specific/' + topImage" :max-height="imgMaxHeight" class="white--text align-end"></v-img>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-3">
      <v-col xs="12" sm="12" md="11" lg="11" xl="11">
        <NotificationSimpleCard
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :citycode="citycode"
          :item="item"
          :icon="'$IconInformation2t'"
        />
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-3">
      <v-col xs="12" sm="12" md="11" lg="11" xl="11">
        <v-row justify="center" :dense="$vuetify.breakpoint.mobile">
          <v-col
            v-for="(item, i) in mainButtons"
            :key=i
            cols="6" xs="6" sm="6" md="3" lg="3" xl="3"
          >
            <HomeMainMenuButton
              :i="i"
              :to="item.to"
              :imgFile="item.imgFile"
              :icon="item.icon"
              :size="$vuetify.breakpoint.mobile ? '40px': '70px'"
              :height="$vuetify.breakpoint.mobile ? '100': '200'"
              :title="item.title"
              :type="item.type"
              buttonRounded="rounded-lg"
              buttonAlign="vertical-align"
              :buttonPadding="$vuetify.breakpoint.mobile ? 'py-4 px-1':'py-10'"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row justify="center" :style="$vuetify.breakpoint.mobile ? 'padding-bottom: 30px': 'padding-bottom: 70px'">
      <v-col xs="12" sm="12" md="11" lg="11" xl="11">
        <v-row justify="center">
          <v-col md="6" lg="6" xl="6"
            v-for="(item, i) in subButtons"
            :key=i
            cols="12"
          >
            <HomeMainMenuButton
              :i="i"
              :to="item.to"
              :imgFile="item.imgFile"
              :icon="item.icon"
              :size="$vuetify.breakpoint.mobile ? '30px': '50px'"
              :height="$vuetify.breakpoint.mobile ? '100': '200'"
              :title="item.title"
              :type="item.type"
              buttonRounded="rounded-lg"
              buttonAlign="horizontal-align"
              :buttonPadding="$vuetify.breakpoint.mobile ? 'py-5 px-6' :'py-11 px-14'"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-md-9" v-if="!$auth.loggedIn">
      <v-col xs="12" sm="12" md="11" lg="11" xl="11">
        <LoginCard
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          buttonTextColor="#fff"
          btnClass="rounded-lg px-7 py-5"
          :citycode="citycode"
        />
      </v-col>
    </v-row>
    <!-- <div :class="['my-14', adStyle]">
      <v-row justify="center" class="py-md-15 py-7">
        <v-col xs="12" sm="12" md="7" lg="7" xl="7" align="center">
          <v-row>
            <v-col xs="12" sm="12" md="3" lg="3" xl="3"
              v-for="(item, i) in [1,2,3,4]"
              :key=i
              cols="12"
            >
              <v-img 
                max-height="60"
                max-width="290"
                src="/specific/bnr_dammy.png"
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div> -->
    <div class="pt-16" v-if="!$vuetify.breakpoint.mobile">
      <v-row justify="center" class="pb-10">
          <div class="font-weight-bold">
            アプリのダウンロードはこちらから
          </div>
      </v-row>
      <v-row dense>
        <v-col class="d-flex justify-end">
          <a
            href="https://play.google.com/store/apps/details?id=com.lg_pwd.chigasaki"
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
            href="https://apps.apple.com/app/apple-store/id1660201682?mt=8"
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