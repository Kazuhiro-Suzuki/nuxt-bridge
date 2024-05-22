<template>
    <div>
        テスト
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    head() {
        return {
            title: this.title
        }
    },
    data() {
        return {
            citycode: this.$route.query.citycode,
        }
    },
    computed: {
        ...mapGetters({
            regionData: 'region/getRegion',
        }),
    },
}
</script>
