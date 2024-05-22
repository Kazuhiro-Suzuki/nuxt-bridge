<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <v-col
            v-for="(item, i) in buttons"
            :key=i
          >
            <MainMenuButton
              :i="i"
              :to="item.to"
              :imgFile="item.imgFile"
              :title="item.title"
              :type="item.type"
              color="grey lighten-4"
            />
          </v-col>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import { facilityButton } from '../../model/facilityButton'


export default {
  head() {
    return {
      title: this.title
    }
  },
  data() {
    return {
      title: 'メニュー',
      citycode: this.$route.query.citycode,
      buttons: [
        // {
        //   title: '障害者施設 一覧',
        //   to: `/facility/disabilities?citycode=${this.$route.query.citycode}`,
        //   imgFile: '',
        //   type: '',
        // },
        // {
        //   title: '相談窓口 一覧',
        //   to: `/facility/services?citycode=${this.$route.query.citycode}`,
        //   imgFile: '',
        //   type: '',
        // },
      ]
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
  created(){
    let buttonInfo = facilityButton.find(item => item.city_code ==  this.citycode);
    this.buttons = buttonInfo.buttons
  },
}
</script>
