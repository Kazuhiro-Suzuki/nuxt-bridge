<template>
  <v-container>
    <v-row justify="center" class="pb-14">
        <v-col cols="12">
            <div class="justify-center text-md-h4 text-h5 font-weight-bold">
                {{ title }}
            </div>
        </v-col>
    </v-row>
    <div class="pb-14" >
        <v-row justify="center" class="pb-6" dense>
            <v-col cols="12">
                <div class="text-line justify-center text-md-h5 text-h6 font-weight-bold mb-6 ml-3" :style="textLineStyles">
                    よくある質問
                </div>
                <div>まずはこちらをご確認ください。</div>
            </v-col>
        </v-row>
        <v-row dense>
            <v-col v-for="(questionButton, i) in questionButtons" :key="i" cols="12" sm="6" md="6" lg="6" xl="6">
                <MainMenuButton
                    :to="questionButton.to"
                    :imgFile="questionButton.imgFile"
                    :title="questionButton.title"
                    :type="questionButton.type"
                    :color="darkColor"
                    :outlined="true"
                    BtnClass="rounded-lg"
                />
            </v-col>
        </v-row>
    </div>
    <div>
        <v-row justify="center" class="pb-6" dense>
            <v-col cols="12">
                <div class="text-line justify-center text-md-h5 text-h6 font-weight-bold mb-6 ml-3" :style="textLineStyles">
                    お問い合わせ
                </div>
                <div>問題が解決しない場合は、こちらからお問い合わせください。</div>
            </v-col>
        </v-row>
        <v-row>
            <v-col v-for="(contactButton, i) in contactButtons" :key="i" cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
                <div class="pb-4 font-weight-bold ">{{ contactButton.subtitle }}</div>
                <MainMenuButton
                    :to="contactButton.to"
                    :imgFile="contactButton.imgFile"
                    :title="contactButton.title"
                    :type="contactButton.type"
                    :color="darkColor"
                    :outlined="true"
                    BtnClass="rounded-lg"
                    />
            </v-col>
        </v-row>
    </div>
  </v-container>
</template>

<script>
export default {
  props: {
    baseColor: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    questionButtons: {
      type: Array,
      required: true,
    },
    contactButtons: {
      type: Array,
      required: true,
    },
    darkColor: {
      type: String,
      required: true,
    },
  },
  computed: {
    textLineStyles () {
      return {
        '--background-color': this.darkColor,
      }
    }
  }
}
</script>

<style scoped>
.text-line{
    position: relative;
}
.text-line::before {
    content:"";
    display:inline-block;
    width: 3px;
    height: 25px;
    background-color: var(--background-color);
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: -10px;
}
</style>
