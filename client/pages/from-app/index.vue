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
    await this.$router.push({
      path: '/home',
      query: {
        citycode: query.citycode,
        from: query.from,
        state: query.state,
      }
    })
  }
}
</script>
