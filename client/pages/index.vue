<script>
export default {
  data() {
    return {
      citycode: this.$route.query.citycode
    }
  },
  created() {
    this.$router.push(`/home?citycode=${this.citycode}`)
  }
}
</script>
