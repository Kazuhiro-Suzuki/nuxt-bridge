<template>
  <v-textarea
    v-model="textAreaData"
    outlined
    counter
    :rows="rows"
    :label="label"
    :background-color="backgroundColor"
    :maxlength="maxlength"
    :rules="rules"
    :disabled="disabled"
  ></v-textarea>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      required: true
    },
    maxlength: {
      type: String,
      required: true,
    },
    backgroundColor: {
      type: String,
      required: false,
    },
    rules: {
      type: Array,
      required: false,
    },
    disabled: {
      type: Boolean,
      required: false,
    },
    rows: {
      type: String,
      default: '10',
      required: false,
    },
    data: {
      type: String,
      default: '',
      required: false,
    }
  },
  data() {
    return {
      textAreaData: this.data
    }
  },
  watch: {
    textAreaData: function(value) {
      this.$emit('textAreaData', value)
    }
  }
}
</script>
