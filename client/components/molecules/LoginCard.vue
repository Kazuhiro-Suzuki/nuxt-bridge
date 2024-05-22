<template>
  <v-card 
    elevation="1" 
    class="pa-md-8 rounded-lg"
    :img="bgImage"
    :color="baseColor">
    <v-row class="align-center">
      <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
        <v-card-text>
          <v-row>
            <v-col>
              <div 
                class="font-weight-bold d-flex align-center justify-center justify-md-start" 
                :style="$vuetify.breakpoint.mobile ? 'font-size:16px' : 'font-size:18px'"
              >
                {{ title }}
              </div>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" v-for="(item, i) in items" :key="i">
              <v-row dense>
                <v-col cols="12" xs="12" sm="12" md="4" lg="4" xl="4" class="d-flex align-center justify-center justify-md-start">
                  <div v-if="item.icon!=''">
                    <v-avatar color="white" size="60px">
                      <v-icon :color="darkColor" size="40px" style="border-radius: 0px;">
                        {{ item.icon }}
                      </v-icon>
                    </v-avatar>
                  </div>
                </v-col>
                <v-col cols="12" xs="12" sm="12" md="8" lg="8" xl="8" class="d-flex align-center justify-center">
                  <div class="px-md-1 px-2 text-md-left text-center" :style="$vuetify.breakpoint.mobile ? 'font-size:13px' : 'font-weight: bold; font-size:14px'">
                    {{ item.text }}
                  </div>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
      </v-col>
      <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
        <v-card-actions class="d-flex justify-md-end justify-center pr-md-10">
          <NormalButton
            :text="text"
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
      title: '',
      text: '',
      items:[],
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
    this.title = buttonInfo.title
    this.text = buttonInfo.text
    this.hasBgImage = buttonInfo.hasBgImage
    this.bgPcImagePath = buttonInfo.bgPcImagePath
    this.bgSpImagePath = buttonInfo.bgSpImagePath
    this.items = buttonInfo.items
  }
}
</script>