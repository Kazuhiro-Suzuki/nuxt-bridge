<template>
  <v-container class="container font-style py-0 mt-md-n13 mt-n3">
    <div :class="[bgTopImg,'over-contents']">
      <v-row justify="center" class="pb-2 pt-8">
        <v-col cols="12" class="parent-position">
            <v-carousel 
              hide-delimiters 
              :show-arrows="false"
              cycle
              class="carousel"
              interval="6000"
            >
              <v-carousel-item
                v-for="(item,i) in carouselItems"
                :key="i"
                reverse-transition="new-transition"
                transition="new-transition"
              >
                <img
                  :src="require(`~/static/specific/${item.src}`)"
                  class="responsive-image"
                  alt="Carousel Image"
                />
              </v-carousel-item>
            </v-carousel> 
        </v-col>
      </v-row>
    </div>
    <v-row justify="center" class="pb-3">
      <v-col cols="12">
        <NotificationSimpleCard
          :baseColor="regionData.light_color"
          :darkColor="regionData.dark_color"
          :citycode="citycode"
          :item="item"
          :icon="'$IconInformation2tLightBlue'"
        />
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-3">
      <v-col cols="12">
        <v-row justify="center" :dense="$vuetify.breakpoint.mobile">
          <v-col
            v-for="(item, i) in mainButtons"
            :key=i
            cols="6" xs="6" sm="6" md="3" lg="3" xl="3"
          >
            <HomeMainMenuButton
              :i="i"
              :to="item.to"
              :imgFile="item.imgFile"
              :icon="item.icon"
              :size="$vuetify.breakpoint.mobile ? '40px': '65px'"
              :height="$vuetify.breakpoint.mobile ? '100': '200'"
              :title="item.title"
              :type="item.type"
              buttonRounded="rounded-lg"
              buttonAlign="vertical-align"
              :buttonPadding="$vuetify.breakpoint.smAndDown ? 'py-4 px-10':'py-10 px-13'"
            />
          </v-col>
          <v-col
            v-for="(item, i) in subButtons"
            :key=i
            cols="12" xs="12" sm="12" md="3" lg="3" xl="3"
          >
            <HomeMainMenuButton
              :i="i"
              :to="item.to"
              :imgFile="item.imgFile"
              :icon="item.icon"
              :size="$vuetify.breakpoint.mobile ? '30px': '60px'"
              :height="$vuetify.breakpoint.mobile ? '100': '200'"
              :title="item.title"
              :type="item.type"
              buttonRounded="rounded-lg"
              :buttonAlign="$vuetify.breakpoint.smAndDown ? 'horizontal-align' : 'vertical-align'"
              :buttonPadding="$vuetify.breakpoint.sm ? 'py-5 px-6':'py-10 px-7'"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-md-9" v-if="!$auth.loggedIn">
      <v-col cols="12">
        <LoginCard
          baseColor="white--text"
          darkColor="white"
          btnClass="rounded-lg font-weight-bold"
          :width="$vuetify.breakpoint.mobile ? '90%' : '100%'"
          :buttonTextColor="regionData.dark_color"
          :citycode="citycode"
        />
      </v-col>
    </v-row>
    <div class="pt-16" v-if="!$vuetify.breakpoint.mobile">
      <v-row justify="center" class="pb-10">
          <div class="font-weight-bold">
            アプリのダウンロードはこちらから
          </div>
      </v-row>
      <v-row dense>
        <v-col class="d-flex justify-end">
          <a
            href="https://play.google.com/store/apps/details?id=com.lg_pwd.edogawa"
            target="_blank"
          >
            <v-img
              src="common/android.png"
              :max-height="maxHeight"
              :max-width="maxWidth"
            >
            </v-img>
          </a>
        </v-col>
        <v-col class="d-flex justify-start">
          <a
            href="https://apps.apple.com/app/apple-store/id6464552770?mt=8"
            target="_blank"
          >
            <v-img
              src="common/ios.png"
              :max-height="maxHeight"
              :max-width="maxWidth"
            >
            </v-img>
          </a>
        </v-col>
      </v-row>
    </div>
    <div style="padding-top:95px;" :class="['pb-15', 'over-contents', bgBottomImg]">
      <v-row justify="center">
          <div>
            <v-btn
              @click="$vuetify.goTo(0)"
              height="65"
              width="65"
              depressed
              elevation="2"
              icon
            >
              <LogoImage
                :imgFile="'specific/button-pagetop-edogawa.svg'"
                :size="'65px'"
              />
            </v-btn>
          </div>
      </v-row>
    </div>

    <v-fab-transition>
      <v-btn
        fab
        fixed
        :style="{ bottom: '-10px', right: '-10px' }"
        class="ma-10"
        @click="openDialog"
      >
        <LogoImage
          :imgFile="'specific/button-helpcard-edogawa.svg'"
          :size="'100px'"
        />
      </v-btn>
    </v-fab-transition>
    <v-dialog
      class="transparent"
      v-model="memberDialog"
      v-if="$auth.loggedIn"
      max-width="640"
    >
      <v-img
          :src="require('~/static/specific/helpcard-member-pc.png')"
      ></v-img>
      <v-card>
        <v-card-text>
          <v-row justify="center">
            <v-col cols="12">
              <v-col cols="12">
                <div class="font-weight-bold">氏名</div>
                <div>{{userInfo.last_name + userInfo.first_name}}</div>
              </v-col>
              <v-divider/>
              <v-col cols="12">
                <div class="font-weight-bold">連絡先</div>
                <div>{{userInfo.phone_number}}</div>
              </v-col>
              <v-divider/>
              <v-col cols="12">
                <div class="font-weight-bold">障害・病気等の内容</div>
                <div>{{userInfo.note1}}</div>
              </v-col> 
              <v-divider/>
              <v-col cols="12">
                <div class="font-weight-bold">知ってほしいこと</div>
                <div>{{userInfo.note2}}</div>
              </v-col> 
              <v-divider/>
              <v-col cols="12">
                <div class="font-weight-bold">配慮事項</div>
                <span 
                  v-for="(item, i) in userInfo.disability_category"
                  :key="i"
                >
                  ・{{item}}
                </span>
              </v-col>
              <v-divider/>
              <v-col cols="12">
                <div class="font-weight-bold">配慮してほしいこと</div>
                <div>{{userInfo.note3}}</div>
              </v-col> 
              <v-divider/>
              <v-col cols="12" class="d-flex justify-end">
                  <LinkButton
                    :path="'/account/profile?citycode='+regionData.city_code"
                    text="編集"
                    :color="regionData.dark_color"
                  />
              </v-col>
              <v-divider class="border-over-contents"/>
              <v-col xs="12" >
                <v-btn
                  x-large
                  elevation="1"
                  dark
                  class="font-weight-bold rounded-lg"
                  :color="regionData.dark_color"
                  :loading="downloadingPdf"
                  width="100%"
                  @click="downloadPdf"
                >
                  ヘルプカードをダウンロード
                </v-btn>
              </v-col>
              <v-col cols="12" class="d-flex justify-center">
                  <TextButton
                    text="閉じる"
                    :color="regionData.dark_color"
                    @clickEvent1="memberDialog = !memberDialog"
                  />
              </v-col>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="publicDialog"
      max-width="640"
    >
      <v-card style="border-radius:15px;">
        <v-img
          :src="require('~/static/specific/helpcard-guide-pc-edogawa.png')"
        ></v-img>
        <v-card-text class="font-style">
          <v-row justify="center">
            <v-col cols="12" class="px-0">
              <v-col cols="12">
                  <p>ヘルプカードをスマホに登録して、困ったときにいつでも提示することができます。</p>
                  <p class="ma-0">カードを持ち歩く必要がないので、紛失する心配もなくなり安心です。</p>
              </v-col>
              <v-col cols="12" style="font-size: 14px;">
                <div class="bg-help-card-color rounded-lg pa-4">
                  <p class="font-weight-bold mb-1">ヘルプカードとは？</p>
                  <p class="mb-1">障害のある方などが、困ったときに、周りの方に助けをお願いするためのものです。</p>
                  <v-btn
                    class="font-weight-bold pa-0"
                    text
                    target="_blank"
                    href="https://www.city.edogawa.tokyo.jp/e041/kenko/fukushikaigo/shogaisha/kenriyogo/helpcard.html"
                    :color="regionData.dark_color"
                  >
                    <span class="text-decoration-underline">詳しくはこちら</span>
                    <v-icon size="16px" :color="regionData.dark_color">$IconNewwindowLine</v-icon>
                  </v-btn>
                </div>
              </v-col>
              <v-col cols="12">
                <div class="d-flex justify-center">
                  <v-btn
                      large
                      elevation="1"
                      :to="'/account?citycode='+regionData.city_code"
                      :color="regionData.dark_color"
                      class="font-weight-bold rounded-lg"
                      dark
                      width="100%"
                  >
                      会員登録(ログイン)して利用
                  </v-btn>
                </div>
              </v-col>
              <v-col cols="12">
                <div class="d-flex justify-center">
                  <TextButton
                    text="閉じる"
                    :color="regionData.dark_color"
                    @clickEvent1="publicDialog = !publicDialog"
                  />
                </div>
              </v-col>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { createSimpleTransition } from 'vuetify/lib/components/transitions/createTransition';
import { homeButton } from '@/model/homeButton'
import { mapGetters } from 'vuex'

export default {
  head() {
    return {
      title: 'ホーム',
    }
  },
  props: {
    item: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      citycode: this.$route.query.citycode,
      fullPath: this.$route.fullPath,
      maxHeight: 60,
      maxWidth: 150,
      imgMaxHeight: 600,
      mainButtons: [],
      subButtons: [],
      publicDialog: false,
      memberDialog: false,
      downloadingPdf: false,
      carouselItems:[
          {
            src: "top-edogawa-v1.png",
          },
          {
            src: "top-edogawa-v2.png",
          },
          {
            src: "top-edogawa-v3.png",
          },
      ],
      userInfo: {}
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    bgTopImg(){
      if(this.$vuetify.breakpoint.mobile){
        return 'bg-top-sp-img'
      }else{
        return 'bg-top-pc-img'
      }
    },
    bgBottomImg(){
      if(this.$vuetify.breakpoint.mobile){
        return 'bg-bottom-sp-img'
      }else{
        return 'bg-bottom-pc-img'
      }
    },
    adStyle(){
      if(this.$vuetify.breakpoint.mobile){
        return 'breaking-mobile-out'
      }
      return 'breaking-out'
    }
  },
  methods: {
    openDialog(){
      if(this.$auth.loggedIn){
        this.memberDialog = true
      }else{
        this.publicDialog = true
      }
    },
    async downloadPdf() {
      this.downloadingPdf = true
      const sleep = msec => new Promise(resolve => setTimeout(resolve, msec))
      try {
        const res = await this.$api.createHelpCardPDF()
        const token = res.data.token
        const id = res.data.id
        while (true) {
          try {
            const response = await this.$api.getHelpCardPDF(`token=${token}&id=${id}`)
            console.log(response);
            window.location.href = response.data
            // console.log(response);
            // const blob = new Blob([response.data], { type: 'application/pdf' })
            
            // const fileName = token + '.pdf'

            // //IE判定
            // if (navigator.msSaveOrOpenBlob) {
            //   navigator.msSaveOrOpenBlob(blob, fileName)
            // } else {
            //   const objectUrl = (window.URL || window.webkitURL).createObjectURL(blob)
            //   const a = document.createElement('a')
            //   a.href = objectUrl
            //   a.download = fileName
            //   document.body.appendChild(a)
            //   a.click()
            //   document.body.removeChild(a)
            // }
            break
          } catch (e) {
            console.log(e)
            await sleep(1000)
          }
        }

      } catch (e) {
        console.log(e)
      }
      this.downloadingPdf = false
    }
  },
  async created(){
    if (this.$auth.loggedIn) {
      const response = await this.$api.getUserInfo()
      if (response.status = 200) {
        this.userInfo = response.data
      } else {
        if (response.data.detail) {
          await this.$store.dispatch('region/setErrorMessage', response.data.detail)
        } else {
          await this.$store.dispatch('region/setErrorMessage', 'ユーザー情報の取得ができませんでした。時間をおいてやり直してください。')

        }
      }
    }

    let buttonInfo = homeButton.find(item => item.city_code ==  this.citycode);
    this.mainButtons = buttonInfo.mainButtons
    this.subButtons = buttonInfo.subButtons
  },
  // mounted() {
  //   const newTransition = createSimpleTransition('new-transition');
  //   this.$once("hook:components", () => {
  //       newTransition
  //   })
  // }
}
</script>

<style scoped>
.nuxt-profile-link {
   color: black;
}
.responsive-image {
  max-width: 100%;
  height: auto;
}
.container{
    max-width: 960px; 
}
.over-contents{
  margin: 0 calc(50% - 50vw);
	padding: 4px calc(50vw - 50% + 8px);
	width: 100vw;
}
.border-over-contents{
  margin: 0 calc(50% - 50vw);
	padding: 4px calc(50vw);
	width: 100vw;
}
.bg-top-pc-img{
  background: url("/specific/bg-top-pc-edogawa.png");
  background-repeat: no-repeat;
  background-position: top center;
}
.bg-top-sp-img{
  background: url("/specific/bg-top-sp-edogawa.png");
  background-repeat: no-repeat;
  background-position: top center;
  background-size: contain;
}
.bg-bottom-pc-img{
  background: url("/specific/bottom-pc-edogawa.png");
  background-repeat: no-repeat;
  background-position: bottom center;
}
.bg-bottom-sp-img{
  background: url("/specific/bottom-sp-edogawa.png");
  background-repeat: no-repeat;
  background-position: bottom center;
  background-size: contain;
}
.parent-position{
  position: relative
}
.child-position{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
} 
.bg-help-card-color{
  background-color: #F5F5F5;
}
@media (width < 700px){
  .carousel{
    max-width: 600px;
    max-height: 200px;
  }
  .carousel-icon{
    max-width: 120px;
    max-height: 120px;
  }
}
@media (width > 700px){
  .container{
    margin-bottom:-120px;
  }
}

.new-transition-leave-active {
  position: absolute;
}

.new-transition-enter-active,
.new-transition-leave,
.new-transition-leave-to {
  transition: 0.8s;
  opacity: 1;
}

.new-transition-enter,
.new-transition-leave-to {
  opacity: 0;
}

</style>

<style>
 .font-style {
  font-family: 'Hiragino Kaku Gothic';
  font-size: 16px;
 }

.breaking-mobile-out {
	margin-right: calc(50% - 50vw);
	margin-left: calc(50% - 50vw);
  overflow: hidden;
  background: #F5F5F5; 
}
.breaking-out {
	margin-right: calc(50% - 50vw);
	margin-left: calc(50% - 50vw);
  overflow: hidden;
  background: #F5F5F5; 
}
</style>