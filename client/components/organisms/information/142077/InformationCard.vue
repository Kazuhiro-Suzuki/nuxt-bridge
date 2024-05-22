<template>
    <v-row justify="center">
      <v-col cols="12" xs="10" sm="10" md="10" lg="10">
        <v-row justify="center" class="pb-6">
          <v-col cols="12">
              <div class="justify-center text-md-h4 text-h5 font-weight-bold mb-6">
                  {{ title }}
              </div>
          </v-col>
          <v-col cols="12">
              <div>聴覚障がい者等（聴覚障がい者、音声機能障がい者又は言語機能障がい者で身体障害者手帳の交付を受けている方）の自立と社会参加を促進することを目的に手話通訳者、要約筆記者を派遣しています。</div>
          </v-col>
        </v-row>
        <v-row justify="center" class="pb-6" dense>
          <v-col cols="12" class="mb-6">
            <div class="font-weight-bold">対象者（主な方）</div> 
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>1．市内に住所を有する聴覚障がい者等</v-list-item-title>
                <v-list-item-title>2．聴覚障がい者等で構成する市内の団体</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12">
            <div class="font-weight-bold">対象事項（内容）</div> 
            <v-simple-table>
              <template v-slot:default outline>
                <thead>
                  <tr :color="regionData.base_color">
                    <th class="text-left">
                      事項
                    </th>
                    <th class="text-left">
                      内容
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(item, i) in items"
                    :key="i"
                  >
                    <td>{{ item.key }}</td>
                    <td>{{ item.value }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-col>
        </v-row>
        <div>
          <v-row justify="center" class="pb-6" dense>
            <v-col cols="12" class="mb-6">
              派遣日の7日前（土・日・祝日・年末年始を除く）までに次の方法で申請してください。
            </v-col>
          </v-row>
        </div>
        <div class="pb-14" >
          <v-row justify="center" class="pb-6" dense>
            <v-col cols="12" class="mb-6">
              <div class="text-line justify-center text-md-h5 text-h6 font-weight-bold ml-3" :style="textLineStyles">
              フォーム申請の方
              </div>
            </v-col>
            <v-col cols="12">
              <div>以下URLより必要事項を入力の上、送信ください。</div>
            </v-col>
            <v-col cols="12">
              <a :href="formApplyUrl" target="_blank" class="text-wrap">{{ formApplyUrl }}</a>
            </v-col>
          </v-row>
        </div>
        <div class="pb-14" >
          <v-row justify="center" class="pb-6" dense>
            <v-col cols="12" class="mb-6">
              <div class="text-line justify-center text-md-h5 text-h6 font-weight-bold ml-3" :style="textLineStyles">
                  e-kanagawa 電子申請
              </div>
            </v-col>
            <v-col>
              <v-row>
                  <v-col cols="12">
                    <div>手話通訳者派遣申請書</div>
                  </v-col>
                  <v-col cols="12">
                      <a :href="firstDigitalApplyUrl" target="_blank" class="text-wrap">{{ firstDigitalApplyUrl }}</a>
                  </v-col>
              </v-row>
              <v-row>
                  <v-col cols="12">
                    <div>要約筆記者派遣申請書</div>
                  </v-col>
                  <v-col cols="12">
                    <a :href="secondDigitalApplyUrl" target="_blank" class="text-wrap">{{ secondDigitalApplyUrl }}</a>
                  </v-col>
              </v-row>
            </v-col>
          </v-row>
        </div>
        <div class="pb-14" >
          <v-row justify="center" class="pb-6" dense>
            <v-col cols="12" class="mb-6">
              <div class="text-line justify-center text-md-h5 text-h6 font-weight-bold ml-3" :style="textLineStyles">
                  直接持参もしくはファクス申請の方
              </div>
            </v-col>
            <v-col cols="12">
              <div>PDFを印刷し、障がい福祉課に提出又はファクス（0467-82-5157）を送付してください。</div>
            </v-col>
            <v-col cols="12">
              <a :href="faxApplyUrl" target="_blank" class="text-wrap">{{ faxApplyUrl }}</a>
            </v-col>
          </v-row>
        </div>
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
        title: '手話通訳者・要約筆記者の派遣',
        firstDigitalApplyUrl: 'https://dshinsei.e-kanagawa.lg.jp/142077-u/profile/userLogin_initDisplay.action?nextURL=CqTLFdO4voaUqlFGpPvOZ%2B3BB%2BFN7Gi4KMXGdBKterQfdrrJ0c3uG%2FcyOaZzLn967JO6F4%2BmWrSv%0D%0A1FXxyDAFxYzNnOoECHreFqLsJJO%2B9FORzN1A80IfOh%2Falp79cCT4SWaxUJRtH98%3Dc%2B7We56LkcE%3D%0D%0A',
        secondDigitalApplyUrl: 'https://dshinsei.e-kanagawa.lg.jp/142077-u/profile/userLogin_initDisplay.action?nextURL=CqTLFdO4vobOiz02nl1%2B7u3BB%2BFN7Gi4KMXGdBKterQfdrrJ0c3uG%2FcyOaZzLn967JO6F4%2BmWrSv%0D%0A1FXxyDAFxYzNnOoECHreFqLsJJO%2B9FOi9BSGXFz2K6yx9%2B%2BhtE1TmZPtQEL5rzs%3D160Uz66gUTk%3D%0D%0A',
        faxApplyUrl: 'https://www.city.chigasaki.kanagawa.jp/_res/projects/default_project/_page_/001/004/355/R5sinseisyo.pdf',
        formApplyUrl: 'https://d2pksbky2cu9a2.cloudfront.net/e53a3c24-8ba2-45cf-a701-3fd28688b760/142077/75e79a75-dd7b-446f-8d94-6fc2960f2923',
        items: [
          {
            key: '公共機関等',
            value: '公的機関での手続き、相談をするときなど',
          },
          {
            key: '講習会等',
            value: '茅ヶ崎市（行政機関を含む。）が主催、共催、後援する講習会、研修会、説明会、事業等に参加をするときなど',
          },
          {
            key: '医療機関',
            value: '病院へ通院をするときなど',
          },
          {
            key: '学校、幼稚園等',
            value: '子どもの通園・通所・通学する学校等の行事に参加をするときなど',
          },
          {
            key: '就職活動等',
            value: '採用説明会や面接に参加をするときなど',
          },
          {
            key: '冠婚葬祭',
            value: '親族の冠婚葬祭の相談、手続き、出席をするときなど',
          },
          {
            key: '地域活動等',
            value: 'まちぢから協議会、自治会連合会及びその構成員である各団体の活動に参加をするときなど',
          },
        ]
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    textLineStyles () {
      return {
        '--background-color': this.regionData.dark_color,
      }
    },
  },
  methods: {
    tel(phoneNumber) {
      window.location.href = `tel:${phoneNumber}`
    },
  }
}
</script>

<style scoped>
.text-line{
    position: relative;
}
.text-line::before {
    content:"";
    display:inline-block;
    width: 3px;
    height: 25px;
    background-color: var(--background-color);
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: -10px;
}
tbody tr:hover {
  background-color: transparent !important;
}
.v-list-item__title{
  overflow:visible
}

.text-wrap{
  word-wrap: break-word;
}
</style>
