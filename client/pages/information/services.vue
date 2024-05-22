<template>
  <v-container>
    <v-row justify="center">
      <v-col sm="10" md="8" lg="8" xl="8">
        <v-card>
          <DenseToolBar
            :baseColor="regionData.base_color"
            :title="title"
          />
          <v-card-text>
            <p class="text--primary">※各項目を押すと外部サイト（港区ホームページ）に移動します。</p>
            <v-row justify="center">
              <v-col cols="12" v-for="category in catgeories"
                :key="category.catgeoryTitle">
                <v-card v-if="category.catgeoryTitle">
                  <v-card class="elevation-0 lighten-4 font-weight" :color='regionData.base_color'>
                    <v-card-title>{{ category.catgeoryTitle }}</v-card-title>
                  </v-card>
                  <v-card-text>
                    <v-row justify="center">
                      <v-col
                        v-for="(item, i) in category.buttons"
                        :key=i
                        cols="12"
                      >
                        <MainMenuButton
                          :i="i"
                          :to="item.to"
                          :imgFile="item.imgFile"
                          :title="item.title"
                          :type="item.type"
                          color="grey lighten-4"
                          :showCaption="false"
                        />
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
                <v-row justify="center" v-else>
                  <v-col
                    v-for="(item, i) in category.buttons"
                    :key=i
                    cols="12"
                  >
                    <MainMenuButton
                      :i="i"
                      :to="item.to"
                      :imgFile="item.imgFile"
                      :title="item.title"
                      :type="item.type"
                      color="grey lighten-4"
                      :showCaption="false"
                    />
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
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
      title: 'サービス別検索',
      citycode: this.$route.query.citycode,
      catgeories: [
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '主な相談窓口',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/madoguchi/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '障害者総合支援法・児童福祉法に基づくサービス',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/jiritsu/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '手帳',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/techo/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '手当・年金',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/teate/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '医療',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/iryo/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '日常生活の支援',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/nichijosekatsu/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '介護・派遣など',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/kaigo/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '社会参加・レクリエーション',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shakaisanka/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '点字・テープなど',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/tenji/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '職業相談・訓練など',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shokugyo/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '住宅',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/jutaku/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '税の減免など',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/genmen/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '割引・減免',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/waribiki/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '障害保健福祉センターの主な事業',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/fukushicenter/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '精神障害者支援センターの主な事業',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/s-shiencenter/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '児童発達支援センターの主な事業',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/jidou-hattatsu/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '港区社会福祉協議会の主な事業',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/kyogikai/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '障害者施設など',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shisetsu/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: 'その他の東京都の施設など',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/to-shisetsu/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '参考資料',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shiryo/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '障害者のためのサービス一覧',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/service.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '心のバリアフリー推進事業',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/kokorobf/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '障害者優先調達推進法',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/chotatsu/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '障害者に関するシンボルマーク',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/mark.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '',
          buttons: [
            {
              title: '障害福祉サービス事業者等の方へ',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/jigyosha/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
      ]
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
  },
}
</script>
