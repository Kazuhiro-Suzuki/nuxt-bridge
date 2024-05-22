<template>
  <v-row>
    <v-col cols="12" style="min-height: 50vh">
      <div class="q-title">
        <span>{{ title }}</span>
      </div>
      <div style="max-width: 720px; margin: 24px auto">
        <variable-form ref="test_form" />
      </div>
    </v-col>
  </v-row>
</template>

<script>
//import draggable from 'vuedraggable'
//function heardCopy(data){return JSON.parse(JSON.stringify(data))}
import variableForm from "@/components/organisms/support-file/VariableForm.vue";
import answerPageOperation from "@/components/organisms/support-file/AnswerPageOperation.vue"

export default {
  name: "App",
  components: {
    variableForm,
    answerPageOperation
  },
  props: {
    isPreview: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: ""
    }
  },
};
</script>

<style scoped lang="scss">
.q-title {
  height: 65px;
  background: #4266ad 0% 0% no-repeat padding-box;
  opacity: 1;
  text-align: center;
  span {
    text-align: center;
    font: normal normal normal 16px/24px Hiragino Sans;
    letter-spacing: 0px;
    color: #ffffff;
    opacity: 1;
    line-height: 65px;
    font-weight: 600;
  }
}
.p-title {
  text-align: left;
  font: normal normal normal 24px/36px Hiragino Sans;
  letter-spacing: 0px;
  color: #212121;
  opacity: 1;
  font-weight: 600;
}
.next-btn {
  width: 180px;
  height: 52px !important;
  background: #2f66d0 0% 0% no-repeat padding-box !important;
  border-radius: 8px;
  opacity: 1;

  text-align: center;
  font: normal normal normal 16px/16px Hiragino Sans;
  letter-spacing: 0px;
  color: #ffffff;
  font-weight: 600;
}

.back-btn {
  width: 180px;
  height: 52px !important;
  background: #ffffff 0% 0% no-repeat padding-box !important;
  border-radius: 8px;
  opacity: 1;

  text-align: center;
  font: normal normal normal 16px/16px Hiragino Sans;
  letter-spacing: 0px;
  color: #2f66d0;
  font-weight: 600;
}
</style>