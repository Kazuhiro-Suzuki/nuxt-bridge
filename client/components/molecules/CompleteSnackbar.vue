<template>
  <v-snackbar v-model="show">
    {{ message }}
    <template v-slot:action="{ attrs }">
      <v-btn
        text
        v-bind="attrs"
        :color="buttonColor"
        @click="show = false"
      >
        閉じる
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      show: false,
      message: '',
      buttonColor: '',
    }
  },
  created() {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'snackbar/showMessage') {
        this.message = state.snackbar.content
        this.buttonColor = state.snackbar.color
        this.show = true
      }
    })
  }
}
</script>