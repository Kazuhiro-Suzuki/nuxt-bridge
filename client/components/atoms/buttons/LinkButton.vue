<template>
  <v-btn
    text
    :color="color"
    :to="path"
    nuxt
  >{{ text }}</v-btn>
</template>

<script>
export default {
  props: [
    "color",
    "path",
    "text",
  ]
}
</script>