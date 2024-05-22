<template>
  <div>
    少々おまちください
  </div>
</template>

<script>
export default {
  head() {
    return {
      title: 'ミライロID連携'
    }
  },
  async created() {
    const query = this.$route.query
    await this.$axios.$post('/api/v1/app/mirairo/connect/', {
      cityCode: query.citycode,
      code: query.code,
      state: query.state
    })
    this.$notifier.showMessage({ content: 'ミライロIDと連携しました。', color: 'info' })
    await this.$router.push({
      path: '/mirairo/',
      query: {
        citycode: query.citycode
      }
    })
  }
}
</script>
