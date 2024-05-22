<template>
  <img
    :src="require(`~/static/${imgFile}`)"
    :height="height ? height: size"
    :width="width ? width: size"
  />
</template>

<script>
export default {
  props: {
    imgFile: {
      type: String,
      required: true
    },
    size: {
      type: String,
      required: false
    },
    height: {
      type: String,
      required: false
    },
    width: {
      type: String,
      required: false
    }
  },
}
</script>