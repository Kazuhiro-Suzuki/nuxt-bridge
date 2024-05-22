<template>
  <v-container>
    <v-row justify="center">
        <v-col cols="12">
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
                            cols="12"
                        >
                            <MainMenuButton
                            :i="i"
                            :to="item.to"
                            :imgFile="item.imgFile"
                            :title="item.title"
                            :type="item.type"
                            color="grey lighten-4"
                            :showCaption="item.showCaption"
                            />
                        </v-col>
                    </v-card>
                </v-col>
            </v-row>
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
      title: 'サービス一覧',
      citycode: this.$route.query.citycode,
      buttons: [
            {
                title: 'サービス別検索',
                to: `/information/services?citycode=131032`,
                imgFile: '',
                icon: '',
                type: '',
                showCaption: false
            },
            {
                title: `障害別検索`,
                to: '/information/disabilities?citycode=131032',
                imgFile: '',
                icon: '',
                type: '',
                showCaption: false
            },
            {
                title: 'バリアフリーマップ',
                to: `https://www.city.minato.tokyo.jp/hofukukanri/kenko/fukushi/shogaisha/hibakusha/bf-townmap.html`,
                imgFile: '',
                icon: '',
                type: 'href',
                showCaption: true
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
