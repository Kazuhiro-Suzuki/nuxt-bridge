<template>
  <v-btn
    :color="color"
    @click="$emit('clickAction')"
    small
    :disabled="disabled"
  >
    <v-icon>{{ icon }}</v-icon>{{ text }}
  </v-btn>
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
    icon: {
      type: String,
      required: false,
    },
    disabled: {
      type: Boolean,
      required: false,
    }
  }
}
</script>
