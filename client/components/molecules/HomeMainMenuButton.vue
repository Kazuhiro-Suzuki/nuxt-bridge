<template>
  <div>
    <div v-if="type != 'href'">
      <v-btn
        :height="height"
        block
        elevation="1"
        :color="color"
        :to="to"
        :disabled="disabled"
        tile
        :class="[buttonAlign, buttonPadding, buttonRounded, fontStyle,'text-center font-weight-bold']"
      >
        <div v-if="imgFile!='' && icon == ''" :class="buttonAlignStlye">
          <LogoImage
            :imgFile="imgFile"
            :size="size"
          />
        </div>
        <div v-if="icon !=''" :class="buttonAlignStlye">
          <v-icon :size="size">{{ icon }}</v-icon>
        </div>
        <div :style="$vuetify.breakpoint.mobile ? 'font-size:12px' : 'font-size:16px'">
          {{ title }}
        </div>
        <div v-if="imgFile!='' && icon != ''" 
          :class="[buttonAlignStlye, 'pl-5']">
          <LogoImage
            :imgFile="imgFile"
            :width="$vuetify.breakpoint.mobile ? '143' : '215'"
          />
        </div>
      </v-btn>
    </div>
    <div v-else>
      <v-btn
        :height="height"
        block
        elevation="1"
        :color="color"
        :href="to"
        :disabled="disabled"
        target="_blank"
        :class="[buttonAlign, buttonPadding, buttonRounded, fontStyle,'text-center font-weight-bold parent-position']"
      >
        <div v-if="imgFile!=''">
          <LogoImage
            :imgFile="imgFile"
            :size="size"
          />
        </div>
        <div v-if="icon !=''" :class="buttonAlignStlye">
          <v-icon :size="size">{{ icon }}</v-icon>
        </div>
        <div :style="$vuetify.breakpoint.mobile ? 'font-size:12px' : 'font-size:16px'">
          {{ title }}
        </div>
        <div class="child-position">
          <v-icon :size="$vuetify.breakpoint.mobile ? '12px' : '20px'" :color="baseColor">$IconNewwindowLine</v-icon>
        </div>
      </v-btn>
      <!-- <span class="caption">{{ notice }}</span> -->
    </div>
  </div>
</template>

<script>
export default {
  props: {
    i: {
      type: Number,
      required: false,
    },
    to: {
      type: String,
      required: false,
    },
    imgFile: {
      type: String,
      required: false,
    },
    icon: {
      type: String,
      required: false,
    },
    size: {
      type: String,
      required: false,
      default: '35'
    },
    height: {
      type: String,
      required: false,
      default: '100'
    },
    title: {
      type: String,
      required: false,
    },
    type: {
      type: String,
      default: '',
    },
    // color: {
    //   type: String,
    //   required: false,
    //   default: 'white'
    // },
    baseColor: {
      type: String,
      required: false,
    },
    rounded: {
      type: Boolean,
      required: false,
      default: false
    },
    buttonAlign: {
      type: String,
      required: false,
      default: ''
    },
    buttonPadding: {
      type: String,
      required: false,
      default: ''
    },
    buttonRounded: {
      type: String,
      required: false,
      default: ''
    },
  },
  data() {
    return {
      disabled: false,
      notice: '*外部サイトに移動します。',
      color: 'white'
    }
  },
  created() {
    console.log(this.baseColor);
    if (this.title == 'ログイン•会員登録' && this.$auth.loggedIn) {
      this.disabled = true
    }
    if (this.$route.query.citycode == '131032') {
      this.notice = '※外部サイト（港区ホームページ）に移動します。'
    }
  },
  computed: {
    buttonAlignStlye(){
      if(this.buttonAlign !== 'vertical-align'){
        return '';
      }
      if(this.$route.query.citycode == '212172'){
          return 'pb-md-1';
      }else{
        return 'pb-md-5';
      }
    },
    fontStyle(){
      return this.$vuetify.breakpoint.mobile ? '': 'text-subtitle-1'
    }
  }
}
</script>

<style scoped>
.vertical-align >>> .v-btn__content{
  flex-direction: column;
  flex: auto;
}
.vertical-align{
  white-space: normal; 
}
.horizontal-align >>> .v-btn__content{
  justify-content: space-between;
}
.parent-position{
  position: relative
}
.child-position{
  position: absolute;
  top: 0;
  right: 0;
  transform: translate(-50%, -50%);
} 
</style>