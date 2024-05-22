<template>
  <v-container>
    <!-- <chigasaki-info-card v-if="regionData.city_code == '142077'"/>
    <minato-info-card v-if="regionData.city_code == '131032'"/> -->
    <component :is="informationComponent" />
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      citycode: this.$route.query.citycode,
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    informationComponent() {
      console.log(this.citycode);
      return () => import(`@/components/organisms/information/${this.citycode}/InformationCard.vue`);
    }
  },
}
</script>