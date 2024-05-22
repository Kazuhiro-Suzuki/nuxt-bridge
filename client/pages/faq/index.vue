<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" v-if="['131032'].includes(citycode)">
        <FaqCard
          :baseColor="regionData.base_color"
          title="よくある質問"
          :buttons="buttons"
        />
      </v-col>
      <v-col cols="12" xs="10" sm="10" md="10" lg="10" v-else>
        <FaqHome
          :baseColor="regionData.base_color"
          title="お問い合わせ・よくある質問"
          :questionButtons="questionButtons"
          :contactButtons="contactButtons"
          :darkColor="regionData.dark_color"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import { faqButton } from '../../model/faqButton'

export default {
  head() {
    return {
      title: this.title
    }
  },
  data() {
    return {
      title: 'お問い合わせ・よくある質問',
      citycode: this.$route.query.citycode,
      buttons: [],
      questionButtons: [],
      contactButtons:[],
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
  created() {
    let buttonInfo = faqButton.find(item => item.city_code ==  this.citycode);
    this.buttons = buttonInfo.buttons
    this.questionButtons = buttonInfo.questionButtons
    this.contactButtons = buttonInfo.contactButtons
  },
}
</script>
