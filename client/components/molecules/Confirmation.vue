<template>
  <v-card>
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-divider></v-divider>
    <v-card-text>
      <slot name="userInfo"></slot>
    </v-card-text>
    <v-card-actions class="justify-center">
      <slot name="firstAction"></slot>
      <TextButton
        v-if="!isNormalButton"
        :text="buttonText"
        :color="darkColor"
        @clickEvent1="$emit('clickEvent2')"
      />
      <NormalButton
        :btnClass="btnClass"
        v-if="isNormalButton"
        :text="buttonText"
        :color="darkColor"
        @clickAction="$emit('clickAction1')"
      /> 
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    baseColor: {
      type: String,
      required: true,
    },
    darkColor: {
      type: String,
      required: true,
    },
    buttonText: {
      type: String,
      required: true,
    },
    isNormalButton: {
      type: Boolean,
      required: false,
      default: false
    },
    btnClass: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      titleClass: '',
    }
  },
  created() {
    this.titleClass = `${this.baseColor} lighten-4`
  }
}
</script>