<template>
  <v-app dark>
    <div>
      <v-app-bar
        :clipped-left="clipped"
        fixed
        app
        color="white"
      >
        <v-btn
          depressed
          elevation="0"
          color="white"
        >
          <LogoImage
            :imgFile="imgFile"
            size="40"
          />
          <v-toolbar-title v-text="title" class="text-h6 ml-2 font-weight-bold" />
        </v-btn>
        <v-spacer></v-spacer>
      </v-app-bar>
    </div>

    <v-main :class="backgroundColor">
      <v-container>
        <ErrorAlert :message="errorMessage" />
        <nuxt />
        <CompleteSnackbar />
      </v-container>
    </v-main>

    <Footer
      :fixed="fixed"
      :copyRight="copyRight"
      :footerBaseColor="footerBaseColor"
    />
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import Footer from '~/layouts/footer/Footer.vue'

export default {
  components: {
    Footer,
  },
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: true,
      title: '障がい者アプリ',
      imgFile: 'v.png',
      nowYear: new Date().getFullYear(),
      backgroundColor: 'white',
      footerBaseColor: 'grey lighten-1',
      copyRight: 'All rights reserved.',
      headerPath: '/',
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
      errorMessage: 'region/getErrorMessage',
    }),
  },
  created() {
    if (this.regionData && this.regionData.hasOwnProperty('city_code')) {
      // storeからRegionDataをGETした場合
      this.imgFile = `specific/${this.regionData.header_image}`
      this.title = this.regionData.header_text
      this.backgroundColor = `${this.regionData.base_color} lighten-5`
      this.footerBaseColor = `${this.regionData.base_color} lighten-3`
      this.copyRight = `${this.nowYear} ${this.regionData.name}. All rights reserved.`
   

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
      this.imgFile = `specific/${regionData.header_image}`
      this.title = regionData.header_text
      this.backgroundColor = `${regionData.base_color} lighten-5`
      this.footerBaseColor = `${regionData.base_color} lighten-3`
      this.copyRight = `${this.nowYear} ${regionData.name}. All rights reserved.`

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
