<template>
  <iframe
      loading=”lazy”
      :src="congestionUrl"
      frameborder="0"
      allowtransparency="true"
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
    title: '混雑状況',
    citycode: this.$route.query.citycode,
    token: null
  }
},
computed: {
  ...mapGetters({
    regionData: 'region/getRegion',
  }),
  congestionUrl(){
    if (this.citycode == '131237') {
      let lang = localStorage.getItem("lang")
      return this.microServiceUrls.congestion_url + '/?citycode=' + this.citycode + '&token=' + this.token + '&lang=' + lang
    }
    if (this.citycode == '092134') {
      return this.microServiceUrls.congestion_url + '/?citycode=' + this.citycode + '&token=' + this.token
    }
    return this.microServiceUrls.congestion_url + '/' + this.citycode + '/?token=' + this.token
  }
},
created(){
  if(this.$auth.strategy.token.get()){
    let jwtToken = this.$auth.strategy.token.get().split(' ');
    this.token = jwtToken[1]
  }
  let titleInfo = pageTitle.find(item => item.city_code ==  this.citycode);
  this.title = titleInfo.congestion_title
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