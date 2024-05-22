<template>
  <v-card outlined elevation="1">
    <v-card-text>
      <div>{{ title }}</div>
      <div
        v-if="item.subject.length > subjectMaxLength"
        v-text="item.subject.slice(0,subjectMaxLength)+' ...'"
        class="text-h6 text--primary"
      />
      <div
        v-else
        v-text="item.subject.slice(0,subjectMaxLength)"
        class="text-h6 text--primary"
      />
      <div>
        {{ $moment(item.active_since).format('YYYY-MM-DD HH:mm') }}
      </div>
    </v-card-text>
    <v-divider />
    <v-card-text>
      <div
        style="white-space: pre-wrap;"
        v-text="markdownParser"
      />
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <LinkButton
        :color="linkButtonColor"
        :path="linkPath"
        :text="text"
      />
    </v-card-actions>
  </v-card>
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
  },
  data() {
    return {
      title: "最新のお知らせ",
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
    }
  }
}
</script>