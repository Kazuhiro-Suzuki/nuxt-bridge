<script>
export default {
  data() {
    return {
      citycode: this.$route.query.citycode
    }
  },
  created() {
    this.$router.push(`/mirairo?citycode=${this.citycode}`)
  }
}
</script>
