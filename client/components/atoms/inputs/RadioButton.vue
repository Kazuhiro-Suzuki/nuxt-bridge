<template>
  <v-container fluid>
    <div>{{ label }}</div>
    <v-radio-group
      v-model="radioGroupData"
      :rules="rules"
      row
    >
      <v-radio
        v-for="choice in choices"
        :key="choice.id"
        :label="choice.text"
        :value="choice.id"
        :disabled="!inputMode"
      />
    </v-radio-group>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      radioGroupData: ''
    }
  },
  props: {
    label: {
      type: String,
      required: false
    },
    rules: {
      type: Array,
      required: false
    },
    choices: {
      type: Array,
      required: true
    },
    inputMode: {
      type: Boolean,
      required: false
    }
  },
  watch: {
    radioGroupData: function(value) {
      this.$emit('radioGroupData', [value])
    }
  }
}
</script>
