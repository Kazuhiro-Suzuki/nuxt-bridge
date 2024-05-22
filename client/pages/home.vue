<template>
  <div>
    <component 
      :is="homeComponent" 
      :item="item"
    />
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: 'ホーム',
    }
  },
  data() {
    return {
      citycode: this.$route.query.citycode,
    }
  },
  computed: {
    homeComponent(){
      return () => import(`@/components/main/${this.citycode}/Home.vue`) 
    }
  },
  async asyncData({ route, $api, $nuxt }) {
    let item = {
      subject: 'お知らせはまだありません。',
      body: 'お知らせはまだありません。',
      active_since: '1960-08-30 07:05',
    }
    let errorMessage = ''
    const notification = await $api.getPublicNotification(`city_code=${route.query.citycode}`)
    if (notification) {
      if (notification.status == 200) {
        if (notification.data[0] != null) {
          item = notification.data[0]
        }
      } else {
        if (notification.data.detail) {
          errorMessage = notification.data.detail
        } else {
          errorMessage = 'サーバーエラーです、時間置いてからお試しください'
        }
      }
    } else {
      errorMessage = 'サーバーエラーです、時間置いてからお試しください'
    }
    return {
      item,
      errorMessage,
    }
  },
}
</script>