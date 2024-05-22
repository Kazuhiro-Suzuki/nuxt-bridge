<template>
  <iframe
      loading=”lazy”
      :src="`${microServiceUrls.booklet_url}/?lang=${lang}`"
      frameborder="0"
  ></iframe>  
</template>


<script>
import { mapGetters } from 'vuex'
import { pageTitle } from '@/model/pageTitle'

export default {
  layout: 'iframe',
  head() {
    return {
      title: this.title,
    }
  },
  data() {
    return {
      title: '福祉の案内',
      citycode: this.$route.query.citycode,
      lang: ''
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
  async asyncData({ $api, route }) {
    let lang = localStorage.getItem("lang")
    console.log(lang);
    let microServiceUrls = ''
    let errorMessage = ''
    const response = await $api.getMicroServiceUrls(`city_code=${route.query.citycode}`)
    // console.log(response.data)
    if (response.status === 200) {
      microServiceUrls = response.data
      console.log(microServiceUrls);
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
    return {
      microServiceUrls,
      errorMessage,
      lang
    }
  },
  created() {
    let titleInfo = pageTitle.find(item => item.city_code ==  this.citycode);
    this.title = titleInfo.booklet_title
  },
}
</script>



<style scoped>
iframe{
  position:absolute;
  top:0;
  left:0;
  width:100%;
  height:100%;
}
</style>