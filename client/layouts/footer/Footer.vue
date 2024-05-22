<template>
  <v-footer
    app
    :absolute="!fixed"
    :class="[footerBaseColor, footerClass]"
    :color="footerBaseColor"
  >
    <v-row justify="center" class="pt-3">
      <v-col cols="12" class="pt-0 text-center">
        <span>&copy; {{ copyRight }}</span>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  props: {
    fixed: {
      type: Boolean,
      required: true,
    },
    copyRight: {
      type: String,
      required: true,
    },
    footerBaseColor: {
      type: String,
      required: true,
    },
    footerClass: {
      type: String,
      required: false,
    }
  }
}
</script>
