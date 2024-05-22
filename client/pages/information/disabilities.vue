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
      title: '障害別検索',
      citycode: this.$route.query.citycode,
      catgeories: [
        {
          catgeoryTitle: '愛の手帳',
          buttons: [
            {
              title: '愛の手帳 1度',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/techo1/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: `愛の手帳 2度`,
              to: 'https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/techo2/index.html',
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '愛の手帳 3度',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/techo3/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '愛の手帳 4度',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/techo4/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '視覚障害',
          buttons: [
            {
              title: '視覚障害 1級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shikaku1/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: `視覚障害 2級`,
              to: 'https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shikaku2/index.html',
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '視覚障害 3級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shikaku3/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '視覚障害 4級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shikaku4/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '視覚障害 5級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shikaku5/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '視覚障害 6級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shikaku6/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '聴覚障害',
          buttons: [
            {
              title: '聴覚障害 2級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/chokaku2/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: `聴覚障害 3級`,
              to: 'https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/chokaku3/index.html',
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '聴覚障害 4級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/chokaku4/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '聴覚障害 6級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/chokaku6/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '平衡障害',
          buttons: [
            {
              title: '平衡障害 3級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/heko3/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: `平衡障害 5級`,
              to: 'https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/heko5/index.html',
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '音声・言語・そしゃく障害',
          buttons: [
            {
              title: '音声言語 3級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/gengo3/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: `音声言語 4級`,
              to: 'https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/gengo4/index.html',
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '肢体不自由',
          buttons: [
            {
              title: '肢体不自由 1級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shitai1/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: `肢体不自由 2級`,
              to: 'https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shitai2/index.html',
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '肢体不自由 3級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shitai3/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '肢体不自由 4級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shitai4/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '肢体不自由 5級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shitai5/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '肢体不自由 6級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/shitai6/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '内部障害',
          buttons: [
            {
              title: '内部障害 1級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/naibu1/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: `内部障害 2級`,
              to: 'https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/naibu2/index.html',
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '内部障害 3級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/naibu3/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '内部障害 4級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/naibu4/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
          ]
        },
        {
          catgeoryTitle: '精神障害',
          buttons: [
            {
              title: '精神障害者 1級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/seshin1/index.html`,
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: `精神障害者 2級`,
              to: 'https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/seshin2/index.html',
              imgFile: '',
              icon: '',
              type: 'href',
            },
            {
              title: '精神障害者 3級',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/seshin3/index.html`,
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
              title: '脳性麻痺',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/nosemahi/index.html`,
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
              title: '進行性筋萎縮症',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/kinishuku/index.html`,
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
              title: '特殊疾病（難病）',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/nanbyo/index.html`,
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
              title: '原爆被爆者',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/hibakusha/index.html`,
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
              title: '戦傷病者',
              to: `https://www.city.minato.tokyo.jp/kenko/fukushi/shogaisha/senshobyosha/index.html`,
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
