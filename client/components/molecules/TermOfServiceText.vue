<template>
<v-container>
  <div v-html="text"/>
</v-container>
</template>

<script>
export default {
  data() {
    return {
    }
  },
  props:{
    text: {
      type: String,
      required: false
    },
  }
}
</script>