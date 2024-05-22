<template>
  <v-container justify-center align-center style="max-width: 960px">
    <v-row justify="center">
      <v-col cols="12" class="img-col">
        <v-img :src="'/specific/' + topImage"></v-img>
      </v-col>
      <v-col cols="12" class="title-col">
        成長や支援の記録をつなげていくサポートファイル
      </v-col>
      <v-col cols="12" class="description-col">
        発達に支援が必要なお子さまやご家族が、生涯にわたって継続したよりよい支援を受けるためには、保健・医療・福祉・保育・教育・就労支援などの関係機関が切れ目のない関わりをすることが大切です。
        このファイルを利用することで、ご家族の情報が各関係機関に伝達されることをねらいとしています。
      </v-col>
      <v-col cols="12" class="start-btn-col"><v-btn :to="{ path: '/support-file', query: { citycode: this.citycode }}">はじめる</v-btn></v-col>
      <v-col cols="12" class="login-col">
        ご利用には<span>ログイン</span>が必要です
      </v-col>
      <v-col cols="12" class="help-col">
        <p>
          <a
            href="https://d3k8u7y4yskhx8.cloudfront.net/static-files/rupinasu_manual.pdf"
            target="_parent"
            class="help-link"
          >
            <v-icon>$IconHelpLine</v-icon>使い方
          </a>
        </p>
      </v-col>
    </v-row>
  </v-container>

  <!-- <div>
        るぴなすノート（データがない場合スタート画面表示）
        <NuxtLink :to="{ path: '/support-file', query: { citycode: this.citycode }}">
            はじめる
        </NuxtLink>
    </div> -->
</template>

<script>
import { mapGetters } from "vuex";

export default {
  head() {
    return {
      title: this.title,
    };
  },
  data() {
    return {
      citycode: this.$route.query.citycode,
      topImage: "",
    };
  },
  computed: {
    ...mapGetters({
      regionData: "region/getRegion",
    }),
  },
  created() {
    this.topImage = "support-file-nasushiobara.png";
    // if (this.citycode === "131237") {
    //   this.topImage = "support-file-nasushiobara.png";
    // }
  },
};
</script>

<style lang="scss">
.v-main {
  background-color: #faf5f0;
}
.img-col {
  text-align: -webkit-center;
  .v-image {
    max-width: 500px;
  }
}
.title-col {
  color: #20613c;
  text-align: center;
  font-family: "Hiragino Kaku Gothic ProN";
  font-size: 20px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}
.description-col {
  width: 80%;
  max-width: 600px;
  color: #212121;
  font-family: "Hiragino Kaku Gothic ProN";
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}
.start-btn-col {
  text-align: center;
  .v-btn {
    width: 343px;
    height: 52px;
    padding: 14px 16px;
    justify-content: center;
    align-items: center;
    gap: 8px;
    max-width: 600px;
    border-radius: 12px;
    background: #118c46 !important;
    color: #fff;
    text-align: center;
    font-family: "Hiragino Kaku Gothic ProN";
    font-size: 16px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
  }
}
.login-col {
  color: #212121;
  text-align: center;
  font-family: "Hiragino Kaku Gothic Pro";
  font-size: 14px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  span {
    color: var(--Gray13, #212121);
    font-family: "Hiragino Kaku Gothic Pro";
    font-size: 14px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    text-decoration-line: underline;
  }
}
.help-col {
  text-align: center;
  font-family: "Hiragino Kaku Gothic Pro";
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
  letter-spacing: 0em;
  .help-link {
    color: #118c46;
  }
  .v-icon {
    color: #118c46;
    width: 18px;
    height: 18px;
    padding-bottom: 2px;
    margin-right: 2px;
  }
}
</style>
