<template>
  <v-alert
    type="error"
    v-if="message"
  >
    {{ message }}
  </v-alert>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      default: '',
    }
  }
}
</script>