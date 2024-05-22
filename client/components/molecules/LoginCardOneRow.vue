<template>
  <v-card 
    elevation="1" 
    class="pa-md-8 rounded-lg"
    :img="bgImage"
    :color="baseColor">
    <v-row class="align-center" dense>
      <v-col cols="12" xs="12" sm="12" md="7" lg="7" xl="7">
        <v-card-text>
          <v-row dense class="d-flex align-center">
            <v-col cols="12" xs="12" sm="12" md="2" lg="2" xl="2" class="d-flex align-center justify-center justify-md-start">
              <v-avatar color="white" size="65px">
                <v-icon :color="darkColor" size="40px" style="border-radius: 0px;">
                  $IconNotification2tDarkGreen
                </v-icon>
              </v-avatar>
            </v-col>
            <v-col cols="12" xs="12" sm="12" md="10" lg="10" xl="10" 
              :style="$vuetify.breakpoint.mobile ? 'font-size:16px;' : 'font-size:18px'"
              class="font-weight-bold pl-2 text-align"
            >
              <div>会員になるとさらに便利に♪</div>
              <div class="pt-2">大事な情報をメールでお知らせします。</div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-col>
      <v-col cols="12" xs="12" sm="12" md="5" lg="5" xl="5">
        <v-card-actions class="d-flex justify-md-end justify-center pr-md-10">
          <NormalButton
            text="ログイン/無料会員登録"
            :btnClass="btnClass"
            :color="darkColor"
            :buttonTextColor="buttonTextColor"
            :width="width"
            @clickAction="login"
          />
        </v-card-actions>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { loginButton } from '@/model/loginButton'

export default {
  props: {
    citycode: {
      type: String,
      required: true,
    },
    baseColor: {
      type: String,
      required: true,
    },
    darkColor: {
      type: String,
      required: true,
    },
    buttonTextColor: {
      type: String,
      required: false,
    },
    btnClass: {
      type: String,
      required: false,
    },
    width: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      size: '35',
      text: '',
      hasBgImage: false,
      bgPcImagePath: '',
      bgSpImagePath: ''
    }
  },
  computed:{
    linkPath() {
      return `/account?citycode=${this.citycode}`
    },
    bgImage(){
      if(!this.hasBgImage){
        return ''
      }
      return this.$vuetify.breakpoint.mobile ? require(`~/static/specific/${this.bgSpImagePath}`) : require(`~/static/specific/${this.bgPcImagePath}`)
    }
  },
  methods: {
    login(){
      this.$router.push(`/account?citycode=${this.citycode}`)
    }
  },
  created(){
    let buttonInfo = loginButton.find(item => item.city_code ==  this.citycode);
    this.hasBgImage = buttonInfo.hasBgImage
    this.bgPcImagePath = buttonInfo.bgPcImagePath
    this.bgSpImagePath = buttonInfo.bgSpImagePath
  }
}
</script>

<style scoped>
@media (width < 400px){
  .text-align {
    text-align: center;
  }
}
</style>