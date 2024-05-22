<template>
  <v-col sm="12" md="12" lg="12" xl="12">
    <TextField
      v-if="inputType === 'text'"
      :label="label"
      :disabled="!inputMode"
      :rules="[required === true ? $rules.required : true]"
      @textFieldData="updateAnswerText"
    />
    <TextArea
      v-if="inputType === 'long_text'"
      maxlength="100"
      :label="label"
      :disabled="!inputMode"
      :rules="[required === true ? $rules.required : true]"
      @textAreaData="updateAnswerText"
    />
    <v-row v-if="inputType === 'check'">
      <CheckBox
        :label="label"
        :choices="choices"
        :inputMode="inputMode"
        :rules="[required === true ? $rules.selectArrayRequired : true]"
        @checkboxData="updateAnswerChoice"
      />
    </v-row>
    <v-row v-if="inputType === 'radio'">
      <RadioButton
        :label="label"
        :choices="choices"
        :inputMode="inputMode"
        :rules="[required === true ? $rules.required : true]"
        @radioGroupData="updateAnswerChoice"
      />
    </v-row>
    <SelectBox
      v-if="inputType === 'select'"
      :label="label"
      :choices="choices"
      :inputMode="inputMode"
      :rules="[required === true ? $rules.required : true]"
      @selectBoxData="updateAnswerChoice"
    />
  </v-col>
</template>

<script>
export default {
  props: {
    inputMode: {
      type: Boolean,
      required: true
    },
    id: {
      type: Number,
      required: true
    },
    inputType: {
      type: String,
      required: true
    },
    name: {
      type:String,
      required: false
    },
    label: {
      type: String,
      default: '',
      required: false
    },
    required: {
      type: Boolean,
      required: true
    },
    choices: {
      type: Array,
      required: false
    }
  },
  methods: {
    updateAnswerText(value) {
      this.$emit('answerQuestion', this.id, value, [])
    },
    updateAnswerChoice(value) {
      this.$emit('answerQuestion', this.id, '', value)
    },
  },
}
</script>
