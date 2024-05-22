<template>
    <v-card>
        <DenseToolBar
        :baseColor="regionData.base_color"
        :title="title"
        />
        <v-card-text>
        <div
            style="white-space: pre-wrap;"
            v-text="firstSentence"
        />
        <br />
        <div>
            <a v-if="citycode == '142077'" href="https://www.city.chigasaki.kanagawa.jp/cgi-bin/contacts/t0600400">
              https://www.city.chigasaki.kanagawa.jp/cgi-bin/contacts/t0600400
            </a>
            
            <a v-if="citycode == '131032'" :href="`mailto:${regionData.email}`">
            {{ regionData.email }}
            </a>

            <div v-if="citycode == '131237'">
              <div>{{ regionData.department }}</div>
              <a :href="`tel::${regionData.phone_number}`">
                {{ regionData.phone_number }}
              </a>
            </div>

            <div v-if="['212172', '092134'].includes(citycode)">
              <div>{{ regionData.department }}</div>
              電話番号: <a :href="`tel::${regionData.phone_number}`">
                {{ regionData.phone_number }}
              </a>
            </div>
        </div>
        <br />
        <div
            style="white-space: pre-wrap;"
            v-text="secondSentence"
        />
        </v-card-text>
    </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      title: 'お問い合わせ',
      citycode: this.$route.query.citycode,
      firstSentence: '',
      secondSentence: '',
    }
  },
  computed: {
    ...mapState({
      regionData: state => state.region.regionData
    })
  },
  created() {
    console.log(this.regionData.department);
    this.firstSentence = `
本アプリの使い方や操作に関するお問い合わせは下記までお願いします。
「${this.regionData.header_text}」お問い合わせ`
    this.secondSentence = `皆様の声を反映し、より良いアプリ提供ができるよう、検討してまいります。`
  },
}
</script>
