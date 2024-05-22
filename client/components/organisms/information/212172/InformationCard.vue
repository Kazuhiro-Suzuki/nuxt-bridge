<template>
    <v-row justify="center">
      <v-col cols="12" xs="8" sm="8" md="8" lg="8">
        <v-row class="pb-6">
          <v-col cols="12">
            <v-toolbar
              :color="regionData.base_color"
              :class="`elevation-0 ${regionData.base_color} font-weight-bold`"
            >
              <v-toolbar-title class="mx-auto">{{ title }}</v-toolbar-title>
            </v-toolbar>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-toolbar
              dense
              :color="regionData.base_color"
              :class="`elevation-0 ${regionData.base_color} mb-5`"
            >
              <v-toolbar-title :style="fontSize">飛騨市地域生活安心支援センター「ふらっと」</v-toolbar-title>
            </v-toolbar>
            <div>設置者：飛騨市</div>
            <div>住所：飛騨市古川町若宮2丁目1番60号</div>		
            <div>TEL（総合相談）：0577-73-7483（総合相談）</div>			
            <div>TEL（暮らしの相談）：070-2237-7730（一般相談）</div>		
            <div>TEL（ふりーすぺーす）：070-2236-9396（居場所）</div>		
            <div>URL：<a href="https://www.city.hida.gifu.jp/site/sougouhukusi/43050.html" class="text-wrap" target="_black">https://www.city.hida.gifu.jp/site/sougouhukusi/43050.html</a></div>		
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-toolbar
              dense
              :color="regionData.base_color"
              :class="`elevation-0 ${regionData.base_color} mb-5`"
            >
              <v-toolbar-title :style="fontSize">その他公共機関</v-toolbar-title>
            </v-toolbar>
            <div>・こころの健康相談</div>
            <div>TEL：0577-33-1111</div>		
            <div>※主治医のいない方が対象、予約必須</div>			
            <div>・こころの相談室</div>		
            <div>TEL：0577-73-2948</div>		
            <div>※予約必須</div>		
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-toolbar
              dense
              :color="regionData.base_color"
              :class="`elevation-0 ${regionData.base_color} mb-5`"
            >
              <v-toolbar-title :style="fontSize">いこい</v-toolbar-title>
            </v-toolbar>
            <div>設置者：社会福祉法人 吉城福祉会</div>
            <div>住所：飛騨市古川町下気多990番地</div>		
            <div>TEL：0577-73-0160</div>			
            <div>FAX：0577-73-0170	</div>		
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-toolbar
              dense
              :color="regionData.base_color"
              :class="`elevation-0 ${regionData.base_color} mb-5`"
            >
              <v-toolbar-title :style="fontSize">相談支援センター まごの手</v-toolbar-title>
            </v-toolbar>
            <div>設置者：株式会社ななほし	</div>
            <div>住所：飛騨市神岡町殿606-2</div>		
            <div>TEL：0578-84-0022</div>			
            <div>FAX：0578-84-0024</div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-toolbar
              dense
              :color="regionData.base_color"
              :class="`elevation-0 ${regionData.base_color} mb-5`"
            >
              <v-toolbar-title :style="fontSize">地域生活支援センター ぷりずむ</v-toolbar-title>
            </v-toolbar>
            <div>設置者：社会福祉法人 飛騨慈光会</div>
            <div>住所：高山市天満町4-64-8 第一ビル1F</div>		
            <div>TEL：0577-32-8736</div>			
            <div>FAX：0577-32-6281</div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-toolbar
              dense
              :color="regionData.base_color"
              :class="`elevation-0 ${regionData.base_color} mb-5`"
            >
              <v-toolbar-title :style="fontSize">地域活動支援センター やまびこ</v-toolbar-title>
            </v-toolbar>
            <div>設置者：特定医療法人 生仁会</div>
            <div>住所：高山市国府町村山251-2</div>		
            <div>TEL：0577-72-5023</div>			
            <div>FAX：0577-72-5024</div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  head() {
    return {
      title: this.title
    }
  },
  data(){
    return {
        title: '各種相談窓口',
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    fontSize(){
      if(this.$vuetify.breakpoint.mobile){
        return {
          'font-size': '14px'
        }
      }
    }
  },
}
</script>

<style scoped>
.text-wrap{
  word-wrap: break-word;
}
</style>
