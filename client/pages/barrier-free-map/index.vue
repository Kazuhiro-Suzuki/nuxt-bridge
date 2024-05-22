<template>
    <iframe
        loading=”lazy”
        :src="microServiceUrls.barrier_free_map_url"
        frameborder="0"
    ></iframe>  
</template>


<script>
import { mapGetters } from 'vuex'

export default {
  layout: 'iframe',
  head() {
    return {
      title: 'やさしいマップちがさき',
    }
  },
  data() {
    return {
      title: 'やさしいマップちがさき',
    }
  },
  async asyncData({ $api, route }) {
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