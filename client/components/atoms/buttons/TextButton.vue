<template>
  <v-btn
    text
    :color="color"
    :disabled="disabled"
    @click="$emit('clickEvent1')"
  >{{ text }}</v-btn>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      required: true,
    },
    disabled: {
      type: Boolean,
      required: false,
    }
  }
}
</script>