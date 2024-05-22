<template>
  <v-toolbar
    dense
    :color="baseColor"
    :class="`elevation-0 ${baseColor} lighten-4 font-weight`"
  >
    <v-toolbar-title>{{ title }}</v-toolbar-title>
  </v-toolbar>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    },
    baseColor: {
      type: String,
      required: true,
    },
  },
}
</script>