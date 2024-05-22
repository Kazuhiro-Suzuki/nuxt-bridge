<template>
  <div>
    <p>{{ title }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: 'アカウント情報',
      citycode: this.$route.query.citycode,
    }
  }
}
</script>