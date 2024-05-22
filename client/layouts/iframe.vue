<template>
  <v-app dark>
    <Header
      :miniVariant="miniVariant"
      :staffItems="staffItems"
      :userItems="userItems"
      :clipped="clipped"
      :fixed="fixed"
      :title="title"
      :imgFile="imgFile"
      :headerPath="headerPath"
      :navClass="navigationBaseColor"
      :darkColor="darkColor"
      :baseColor="baseColor"
      :citycode="citycode"
    />

    <v-main :class="backgroundColor">
      <v-container class="pt-md-13" :style="$vuetify.breakpoint.mobile ? '' : 'margin-bottom: 120px'">
        <ErrorAlert :message="errorMessage" />
        <nuxt />
        <CompleteSnackbar />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
import Header from '~/layouts/header/Header.vue'
import Footer from '~/layouts/footer/Footer.vue'
import FooterBgImage from '~/layouts/footer/FooterBgImage.vue'
import { sideBarButton } from '../model/sideBarButton'

export default {
  components: {
    Header,
    FooterBgImage,
    Footer,
  },
  head(){
    return {
      titleTemplate: this.titleTemplate
    }
  },
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: true,
      staffItems: [],
      userItems: [],
      facilityItems: [],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: '障がい者アプリ',
      imgFile: 'v.png',
      footerPcImg: '',
      footerSpImg: '',
      nowYear: new Date().getFullYear(),
      backgroundColor: 'white',
      navigationBaseColor: 'grey lighten-1',
      darkColor: 'white',
      baseColor: 'white',
      copyRight: 'All rights reserved.',
      headerPath: '/',
      citycode: '',
      titleTemplate: '',
      footerClass: '',
      defaultContainerClass: '',
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
      errorMessage: 'region/getErrorMessage',
    }),
  },
  async created() {
    if (this.regionData && this.regionData.hasOwnProperty('city_code')) {
      let buttonInfo = sideBarButton.find(item => item.city_code ==  this.regionData.city_code);
      this.userItems = buttonInfo.userItems
      this.staffItems = buttonInfo.staffItems
      this.facilityItems = buttonInfo.facilityItems
      // storeからRegionDataをGETした場合
      this.headerPath = `/home?citycode=${this.regionData.city_code}`
      this.imgFile = `specific/${this.regionData.header_image}`
      this.title = this.regionData.header_text
      this.copyRight = `${this.nowYear} ${this.regionData.name}. All rights reserved.`
      this.citycode = this.regionData.city_code
      this.footerPcImg = this.regionData.footer_pc_image
      this.footerSpImg = this.regionData.footer_sp_image
     if(['131032'].includes(this.citycode)){
        this.backgroundColor = `${this.regionData.base_color} lighten-5`
        this.navigationBaseColor = `${this.regionData.base_color} lighten-3`
        this.footerBaseColor = `${this.regionData.base_color} lighten-3`
        this.titleTemplate = '%s - 障害者支援アプリ'
        this.defaultContainerClass = 'pt-md-13'
      }
      if(['142077', '131237', '212172', '092134'].includes(this.citycode)){
        this.backgroundColor = `white lighten-5`
        this.navigationBaseColor = `white lighten-3`
        this.footerBaseColor = `${this.regionData.base_color}`
        this.darkColor = this.regionData.dark_color
        this.baseColor = this.regionData.base_color
        this.titleTemplate = '%s - 障がい者支援アプリ'
        this.footerClass = 'py-6 white--text'
        this.fixed = false
        this.defaultContainerClass = 'pt-md-13'
      }

      if(['131237'].includes(this.citycode)){
        // this.defaultContainerClass = 'pb-0 pt-0'
        this.defaultContainerClass = 'pb-0 pt-md-13'
        this.titleTemplate = '%s - ミライク -MIRAIKU-'
      }

      // faviconの動的差し替え
      const favicon = document.querySelector("link[rel*='icon']") || document.createElement('link')
      favicon.type = 'image/x-icon'
      favicon.rel = 'shortcut icon'
      favicon.href = 'specific/' + this.regionData.header_image
      document.getElementsByTagName('head')[0].appendChild(favicon)

    } else {
      // storeのセットが間に合わず、pageからRegionData受け取った場合
      this.setListener()
    }
  },
  methods: {
    setListener() {
      this.$nuxt.$on('updateLayout', this.setLayout)
    },
    setLayout(regionData) {
      this.headerPath = `/home?citycode=${regionData.city_code}`
      this.imgFile = `specific/${regionData.header_image}`
      this.title = regionData.header_text
      this.backgroundColor = `${regionData.base_color} lighten-5`
      this.navigationBaseColor = `${regionData.base_color} lighten-3`
      this.citycode = regionData.city_code
      this.footerBaseColor = `${regionData.base_color} lighten-3`
      this.copyRight = `${this.nowYear} ${regionData.name}. All rights reserved.`
      Object.keys(this.staffItems).forEach(function(value) {
        if (this.staffItems[value]['to'].endsWith('citycode=')) {
          this.staffItems[value]['to'] += regionData.city_code
        }
      }, this)
      Object.keys(this.userItems).forEach(function(value) {
        if (this.userItems[value]['to'].endsWith('citycode=')) {
          this.userItems[value]['to'] += regionData.city_code
        }
      }, this)
      Object.keys(this.facilityItems).forEach(function(value) {
        if (this.facilityItems[value]['to'].endsWith('citycode=')) {
          this.facilityItems[value]['to'] += regionData.city_code
        }
      }, this)

      // faviconの動的差し替え
      const favicon = document.querySelector("link[rel*='icon']") || document.createElement('link')
      favicon.type = 'image/x-icon'
      favicon.rel = 'shortcut icon'
      favicon.href = 'specific/' + regionData.header_image
      document.getElementsByTagName('head')[0].appendChild(favicon)
    },
  },
}
</script>
