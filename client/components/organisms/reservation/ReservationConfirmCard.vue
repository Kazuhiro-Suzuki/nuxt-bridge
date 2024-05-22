<template>
  <div>
    <v-card-text v-if="this.questions.length !== 0">
      <v-form v-model="formValid">
        <v-row v-for="(question, index) in questions" :key="index">
          <answer-form
            :inputMode="mode"
            :inputType="question['type']"
            :id="question['id']"
            :name="question['name']"
            :label="question['displaySentence']"
            :required="question['required']"
            :choices="question['choices']"
            @answerQuestion="answerQuestion"
          />
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions class="justify-space-around">
      <NormalButton
        text="戻 る"
        color="grey lighten-2"
        @clickAction="back"
      />
      <NormalButton
        v-show="this.mode && this.questions.length !== 0"
        text="入力内容を確認する"
        :color="`${this.baseColor} lighten-4`"
        :disabled="!formValid || !$auth.loggedIn"
        @clickAction="changeMode(false)"
      />
      <NormalButton
        v-show="!this.mode || this.questions.length === 0"
        text="予約を確定する"
        :color="`${this.baseColor} lighten-4`"
        :disabled="!formValid || !$auth.loggedIn"
        @clickAction="confirmedReservation"
      />
    </v-card-actions>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mode: true,
      answer: {},
      formValid: false,
    }
  },
  props: {
    citycode: {
      type: String,
      required: true
    },
    baseColor: {
      type: String,
      required: true
    },
    facilityId: {
      type: Number,
      required: true
    },
    temporaryReservationId: {
      type: Array,
      required: true
    },
    questions: {
      type: Array,
      required: true
    }
  },
  methods: {
    answerQuestion(...args) {
      const [id, text, choices] = args
      this.answer[id] = { text: text, choices: choices }
    },
    changeMode(mode) {
      this.mode = mode
    },
    back() {
      if (!this.mode) {
        this.changeMode(true)
      } else {
        this.$router.push(`/reservation/list?citycode=${this.citycode}&facilityId=${this.facilityId}`)
      }
    },
    async confirmedReservation() {
      let surveyResponse = []
      Object.keys(this.answer).forEach(id => {
        surveyResponse.push({
          ...{'questionId': id},
          ...this.answer[id]
        })
      })

      const payload = {
        'email': this.$auth.user.email,
        'temporaryReservationId': this.temporaryReservationId,
        'surveyResponse': surveyResponse
      }
      const response = await this.$api.postReservation(payload)
      if (response.status !== 201) {
        if (response.data.detail) {
          await this.$store.dispatch('region/setErrorMessage', response.data.detail)
        } else {
          await this.$store.dispatch('region/setErrorMessage', '予約ができませんでした、時間をおいてやり直してください。')
        }
        return
      }

      await this.$emit('stopCancelingReservationTmp')

      this.$router.push({
            path: '/reservation/completed',
            query: {
              citycode: this.citycode,
              reservationId: Array.isArray(response.data) ? response.data.map((item)=> item.id).join(',') : response.data['id'],
            }
          })
    },
  },
}
</script>
