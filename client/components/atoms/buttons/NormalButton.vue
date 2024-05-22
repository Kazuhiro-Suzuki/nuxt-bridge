<template>
  <v-btn
    :style="buttonTextStyle"
    :class="btnClass"
    :color="color"
    :width="width"
    @click="$emit('clickAction')"
    large
    :block="block"
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
      required: false,
    },
    buttonTextColor: {
      type: String,
      required: false,
    },
    btnClass: {
      type: String,
      required: false,
    },
    icon: {
      type: String,
      required: false,
    },
    disabled: {
      type: Boolean,
      required: false,
    },
    block: {
      type: Boolean,
      required: false,
    },
    width: {
      type: String,
      required: false,
    }
  },
  computed: {
    buttonTextStyle(){
      return {
        'color': this.buttonTextColor,
      }
    }
  }
}
</script>