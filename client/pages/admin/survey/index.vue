<template>
  <iframe
      loading=”lazy”
      :src="surveyUrl"
      frameborder="0"
      allow="clipboard-write"
  ></iframe>  
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  layout: 'iframe',
  head() {
    return {
      title: 'アンケート管理',
    }
  },
  data() {
    return {
      title: 'アンケート管理',
      citycode: this.$route.query.citycode,
      token: null,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    surveyUrl(){
      console.log(this.microServiceUrls.survey_url + '/' + this.citycode + '/staff?token=' + this.token);
      return this.microServiceUrls.survey_url + '/' + this.citycode + '/staff?token=' + this.token
    }
  },
  created(){
    if(this.$auth.strategy.token.get()){
      let jwtToken = this.$auth.strategy.token.get().split(' ');
      this.token = jwtToken[1]
    }
  },
  async asyncData({ $api, route}) {
    let microServiceUrls = ''
    let errorMessage = ''
    const response = await $api.getMicroServiceUrls(`city_code=${route.query.citycode}`)
    // console.log(response.data)
    if (response.status === 200) {
      microServiceUrls = response.data
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
    return {
      microServiceUrls,
      errorMessage
    }
  }
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