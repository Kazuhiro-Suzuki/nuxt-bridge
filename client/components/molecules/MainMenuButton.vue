<template>
  <div>
    <div v-if="type != 'href'">
      <v-btn
        
        x-large
        block
        elevation="1"
        :color="color"
        :to="to"
        :disabled="disabled"
        :outlined="outlined"
        :class="BtnClass"
      >
        <div v-if="imgFile!=''">
          <LogoImage
            :imgFile="imgFile"
            :size="size"
          />
        </div>
        &nbsp;
        {{ title }}
      </v-btn>
    </div>
    <div v-else>
      <v-btn
        x-large
        block
        elevation="1"
        :color="color"
        :outlined="outlined"
        :class="BtnClass"
        :href="to"
        :disabled="disabled"
        target="_blank"
      >
        <div v-if="imgFile!=''">
          <LogoImage
            :imgFile="imgFile"
            :size="size"
          />
        </div>
        {{ title }}
         &nbsp;
        <div v-if="icon != ''">
          <v-icon :size="20">{{ icon }}</v-icon>
        </div>
      </v-btn>
      <span v-if="showCaption" class="caption">{{ notice }}</span>
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
    title: {
      type: String,
      required: false,
    },
    type: {
      type: String,
      default: '',
    },
    color: {
      type: String,
      required: false,
      default: 'white'
    },
    outlined: {
      type: Boolean,
      required: false,
      default: false
    },
    BtnClass: {
      type: String,
      required: false,
    },
    showCaption: {
      type: Boolean,
      required: false,
      default: true
    },
  },
  data() {
    return {
      size: '35',
      disabled: false,
      notice: '*外部サイトに移動します。',
    }
  },
  created() {
    if (this.title == 'ログイン•会員登録' && this.$auth.loggedIn) {
      this.disabled = true
    }
    if (this.$route.query.citycode == '131032') {
      this.notice = '※外部サイト（港区ホームページ）に移動します。'
    }
  }
}
</script>