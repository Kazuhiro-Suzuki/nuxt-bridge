<template>
  <v-container fluid>
    <div>{{ label }}</div>
    <v-radio-group
      row
    >
      <v-checkbox
        v-for="(choice, index) in choices"
        :key="index"
        v-model="checkboxData"
        :label="choice.text"
        :value="choice.id"
        :rules="rules"
        dense
        :disabled="!inputMode"
        :hide-details="!isFirstItem(index)"
        style="margin-right: 16px;"
      />
    </v-radio-group>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      checkboxData: []
    }
  },
  props: {
    label: {
      type: String,
      required: true
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
    checkboxData: function(value) {
      this.$emit('checkboxData', value)
    }
  },
  methods:  {
    isFirstItem(index) {
      return index === 0
    }
  }
}
</script>
