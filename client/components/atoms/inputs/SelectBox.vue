<template>
  <v-row>
    <v-container fluid>
      <div>{{ label }}</div>
      <v-select
        label="選択してください"
        :rules="rules"
        v-model="selectBoxData"
        :items="choices"
        item-text="text"
        item-value="id"
        single-line
        :disabled="!inputMode"
      >
      </v-select>
    </v-container>
  </v-row>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      required: false
    },
    choices: {
      type: Array,
      required: true
    },
    inputMode: {
      type: Boolean,
      required: false
    },
    rules: {
      type: Array,
      required: false,
    },
  },
  watch: {
    selectBoxData: function(value) {
      this.$emit('selectBoxData', [value])
    }
  },
  data() {
    return {
      selectBoxData: ''
    }
  }
}
</script>
