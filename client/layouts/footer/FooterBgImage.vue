<template>
  <v-footer
    app
    inset
    :absolute="!fixed"
    :class="footerBaseColor"
    padless
  >
    <v-row dense>
      <v-col class="text-center" cols="12" :style="backgroundStyle">
        <span class="footer-text" :style="spanStyle"> &copy; {{ copyRight }}</span>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  data(){
    return {
      pcLineHeight: 27,
      spLineHeight: 15,
      pcFooterTextTop: 50,
      spFooterTextTop: 70,
    }
  },
  props: {
    fixed: {
      type: Boolean,
      required: true,
    },
    copyRight: {
      type: String,
      required: true,
    },
    footerBaseColor: {
      type: String,
      required: true,
    },
    footerPcImg: {
      type: String,
      required: true,
    },
    footerSpImg: {
      type: String,
      required: true,
    },
    citycode: {
      type: String,
      required: true,
    },
  },
  computed: {
    backgroundStyle() {
      return {
        '--background-pc-image': `url('/specific/${this.footerPcImg}')`,
        '--background-sp-image': `url('/specific/${this.footerSpImg}')`,
        '--line-pc-height': this.pcLineHeight,
        '--line-sp-height': this.spLineHeight
      };
    },
    spanStyle(){
      return {
        '--pc-top': `${this.pcFooterTextTop}px`,
        '--sp-top': `${this.spFooterTextTop}px`
      };
    },
  },
  created(){
    if(this.citycode == '092134'){
      this.pcLineHeight = 10
      this.pcFooterTextTop = 40
    }
  }
}
</script>

<style scoped lang="scss">
.v-footer {
  .col {
    line-height: var(--line-pc-height);
    background: var(--background-pc-image);
    background-repeat: repeat-x;
    background-position: center bottom;
    background-color: #FFFFFF;

    @media screen and (max-width: 375px) {
      line-height: var(--line-sp-height);
      background: var(--background-sp-image);
      background-repeat: repeat-x;
      background-color: #FFFFFF;
      background-position: center bottom;
      background-size: 100%;
    }
  }
}
.footer-text{
  text-align: center;
  font: normal normal normal 14px/19px Roboto;
  letter-spacing: 0px;
  color: #999999;
  opacity: 1;
  position: relative;
  top: var(--pc-top);
  @media screen and (max-width: 375px) {
    top: var(--sp-top);
  }
}
</style>
