<template>
  <div>
    <component
      :is="navigationComponent"
      :miniVariant="miniVariant"
      :staffItems="staffItems"
      :userItems="userItems"
      :facilityItems="facilityItems"
      :clipped="clipped"
      :fixed="fixed"
      :navClass="navClass"
      :citycode="citycode"
      :drawer="drawer"
      :darkColor="darkColor"
      :baseColor="baseColor"
      @changeDrawer="changeDrawer"
    />
    <v-app-bar :clipped-left="clipped" fixed app color="white" id="myHeader">
      <v-btn
        v-if="['142077'].includes(citycode) && $vuetify.breakpoint.smAndDown"
        depressed
        fab
        small
        icon
        :disabled="!canBack"
        @click="back()"
      >
        <v-icon v-show="canBack">mdi-arrow-left</v-icon>
      </v-btn>

       <!-- ロゴとアプリ名の表示 パターン1-->
      <v-btn
        v-if="['212172', '092134'].includes(citycode)"
        depressed
        elevation="0"
        color="white"
        @click="$router.push(headerPath)"
      >
        <LogoImage v-if="citycode == '092134'" :imgFile="imgFile" height="60" width="130" />
        <LogoImage v-if="citycode == '212172'" :imgFile="imgFile" size="250" />
      </v-btn>

      <!-- ロゴとアプリ名の表示　パターン2 -->
      <v-btn
        v-else
        :class="['142077'].includes(citycode) ? 'px-0' : ''"
        depressed
        elevation="0"
        color="white"
        @click="$router.push(headerPath)"
      >
        <LogoImage :imgFile="imgFile" size="40" />
        <v-toolbar-title
          v-text="title"
          class="ml-2 font-weight-bold"
          :style="
            $vuetify.breakpoint.smAndUp ? 'font-size: 20px' : 'font-size: 16px'
          "
        />
      </v-btn>

      <v-spacer></v-spacer>
      <v-menu top :close-on-click="true" v-if="['131237'].includes(citycode)">
        <template v-slot:activator="{ on, attrs }">
          <div
            style="width: 100px; text-align: center"
            v-bind="attrs"
            v-on="on"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
            >
              <rect width="24" height="24" fill="none" />
              <path
                d="M8777-5107a10.924,10.924,0,0,1-7.776-3.222A10.925,10.925,0,0,1,8766-5118a10.924,10.924,0,0,1,3.223-7.776A10.924,10.924,0,0,1,8777-5129a10.926,10.926,0,0,1,7.778,3.222A10.924,10.924,0,0,1,8788-5118a10.925,10.925,0,0,1-3.223,7.779A10.926,10.926,0,0,1,8777-5107Zm-2.248-2.285a17.568,17.568,0,0,1-2.709-7.715h-3.986A9.024,9.024,0,0,0,8774.751-5109.285Zm4.5,0a9.023,9.023,0,0,0,6.7-7.714h-3.986A17.568,17.568,0,0,1,8779.249-5109.285Zm-2.25-.269a15.693,15.693,0,0,0,2.95-7.446h-5.9A15.71,15.71,0,0,0,8777-5109.554Zm8.945-9.446a9.021,9.021,0,0,0-6.7-7.715,17.574,17.574,0,0,1,2.709,7.715Zm-6,0a15.679,15.679,0,0,0-2.95-7.446,15.7,15.7,0,0,0-2.948,7.446Zm-7.907,0a17.576,17.576,0,0,1,2.709-7.715,9.021,9.021,0,0,0-6.7,7.715Z"
                transform="translate(-8765 5130)"
                fill="#0099d9"
              />
            </svg>
            <div style="line-height: normal; font-weight: 300; font-size: 12px">
              Language
            </div>
          </div>
        </template>

        <v-list>
          <v-list-item
            v-for="(lang, index) in languages"
            :key="lang.tl + index"
            @click="changeLanguage(lang.tl)"
          >
            <v-list-item-title>{{ lang.label }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        :color="['131237', '212172'].includes(citycode) ? baseColor : ''"
      />
    </v-app-bar>
    <script type="text/javascript">
      function googleTranslateElementInit() {
        new google.translate.TranslateElement(
          {
            pageLanguage: "ja", // Webサイトの言語
            includedLanguages: "en,zh-CN,ko,ja", // 翻訳する言語
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE, // 表示モード
            autoDisplay: false, // 翻訳バナーを自動的に表示するか
            multilanguagePage: true, // コンテンツに複数の言語が含まれているか
            gaTrack: true, // Google Analyticsにより、トラフィックを追跡するか
            gaId: "UA-xx-1", // Google AnalyticsのID
            includeEpub: true,
          },
          "google_translate_element"
        );
      }
    </script>
    <script
      type="text/javascript"
      src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"
    ></script>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    miniVariant: {
      type: Boolean,
      required: true,
    },
    staffItems: {
      type: Array,
      required: true,
    },
    facilityItems: {
      type: Array,
      required: false,
    },
    userItems: {
      type: Array,
      required: true,
    },
    clipped: {
      type: Boolean,
      required: true,
    },
    fixed: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    imgFile: {
      type: String,
      required: true,
    },
    headerPath: {
      type: String,
      required: true,
    },
    navClass: {
      type: String,
      required: true,
    },
    citycode: {
      type: String,
      required: true,
    },
    darkColor: {
      type: String,
      required: false,
    },
    baseColor: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      drawer: false,
      languages: [
        { label: "英語", tl: "en" },
        { label: "中国語", tl: "zh-CN" },
        { label: "韓国語", tl: "ko" },
        { label: "日本語", tl: "ja" },
        { label: "タガログ語", tl: "fil" },
        { label: "ヒンズー語", tl: "hi" },
        { label: "ベトナム語", tl: "vi" },
        { label: "ドイツ語", tl: "de" },
        { label: "フランス語", tl: "fr" },
        { label: "イタリア語", tl: "it" },
        { label: "スペイン語", tl: "es" },
        { label: "ポルトガル語", tl: "pt" },
        { label: "ロシア語", tl: "ru" },
      ],
    };
  },
  computed: {
    ...mapState("back", ["canBack", "backTo"]),
    navigationComponent() {
      return () => import(`@/layouts/nav/${this.citycode}/Navigation.vue`);
    },
  },
  methods: {
    changeLanguage(lang) {
      const currentUrl = window.location.href;
      let newUrl = "";
      if (currentUrl.match(/#googtrans/)) {
        newUrl = currentUrl.replace(
          /#googtrans\(ja\|.+\)/,
          `#googtrans(ja|${lang})`
        );
      } else {
        newUrl = currentUrl + `#googtrans(ja|${lang})`;
      }
      localStorage.setItem(
        "lang",
        lang
      );      
      window.location.href = newUrl;
      location.reload();
    },
    logout() {
      this.$auth.logout().then(() => {
        this.$router.push(`/?citycode=${this.citycode}`);
        this.$notifier.showMessage({
          content: "ログアウトしました。",
          color: "info",
        });
      });
    },
    changeDrawer(val) {
      this.drawer = val;
    },
    back() {
      if (this.backTo) {
        this.$router.push(this.backTo);
      } else {
        history.back();
      }
    },
  },
  created() {
    if (this.$device.isDesktop && this.citycode == "131032") {
      this.drawer = true;
    }
  },
  mounted() {
    const currentUrl = window.location.href;
    if (currentUrl.match(/#googtrans/)) {
      const iframe = document.getElementById("myHeader");
      if (iframe) {
        iframe.style.top = "38px";
      }
    }
  },
};
</script>

<style scoped lang="scss">
::v-deep .skiptranslate .goog-te-gadget-simple {
  // display: none !important;
  border-radius: 5px;
}
</style>
