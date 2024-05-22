<template>
  <div class="font-style">
    <v-row class="pb-2">
      <v-col class="d-flex justify-start align-center font-weight-bold">
        <v-icon :color="darkColor">{{ icon }}</v-icon>
        <div class="pl-2">{{ title }}</div>
      </v-col>
      <v-col class="d-flex justify-end align-center ">
        <v-btn
          text
          color="black"
          :to="linkPath"
          nuxt
          class="font-weight-bold px-0"
        >
          {{ text }}
           <v-icon>$IconArrowRight</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-card elevation="1" :color="baseColor" :to="`/notification?citycode=${citycode}`">
      <v-card-text class="black--text">
        <v-row align="center">
          <v-col cols=12 xs="12" sm="12" md="2" lg="2" xl="2"  align-content="center">
            <div>
              {{ $moment(item.active_since).format('YYYY年MM月DD日') }}
            </div>
          </v-col>
          <v-col cols=12 xs="12" sm="12" md="10" lg="10" xl="10">
            <div
              v-if="item.subject.length > subjectMaxLength"
              v-text="item.subject.slice(0,subjectMaxLength)+' ...'"
              class="font-weight-bold"
            />
            <div
              v-else
              v-text="item.subject.slice(0,subjectMaxLength)"
              class="font-weight-bold"
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { marked } from 'marked'
import striptags from "striptags";


export default {
  props: {
    citycode: {
      type: String,
      required: true,
    },
    item: {
      type: Object,
      required: false,
    },
    baseColor: {
      type: String,
      default: "white",
      required: true,
    },
    darkColor: {
      type: String,
      default: "white",
      required: true,
    },
    icon: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      title: "お知らせ",
      linkButtonColor: "blue",
      text: "もっと見る",
      subjectMaxLength: 50,
      bodyMaxLength: 100,
    }
  },
  computed:{
    linkPath() {
      return `/notification?citycode=${this.citycode}`
    },
    markdownParser(){
      marked.setOptions({
        gfm: false,
      });
      const html = marked.parse(this.item.body);
      const text = striptags(html.trim());
      if(text.length > this.bodyMaxLength){
        return text.slice(0, this.bodyMaxLength)+' ...'
      }else {
        return text
      }
    },
  }
}
</script>

<style scoped>
.font-style{
  font-family: 'normal normal normal 40px/68px Hiragino Sans;'
 }
</style>