<template>
  <div>
    <v-card>
      <DenseToolBar
        :title="title"
        :baseColor="baseColor"
      />
      <v-form v-model="formValid">
        <v-card-text>
          <TextField
            label="パスワード"
            maxlength="50"
            icon="mdi-lock"
            type="password"
            :rules="[$rules.required]"
            @textFieldData="setPassword"
          />
          <TextField
            label="パスワード"
            maxlength="50"
            icon="mdi-lock"
            type="password"
            :rules="[$rules.required]"
            @textFieldData="setPasswordReconfirm"
          />
        </v-card-text>
        <v-card-actions class="justify-center">
          <NormalButton
            text="変更する"
            icon="mdi-lock"
            :class="`${baseColor} lighten-4`"
            :color="baseColor"
            @clickAction="resetPassword"
          />
        </v-card-actions>
      </v-form>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: false,
    },
    citycode: {
      type: String,
      required: true,
    },
    baseColor: {
      type: String,
      required: false,
    },
    uid: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      formValid: false,
      data: {
        password: '',
        password_reconfirm: '',
        uid: '',
      }
    }
  },
  methods: {
    setPassword(value) {
      this.data.password = value
    },
    setPasswordReconfirm(value) {
      this.data.password_reconfirm = value
    },
    async resetPassword() {
      this.data.uid = this.uid
      const response = await this.$api.postResetPassword(this.data)
      // console.log(response)
      if (response.status == 200) {
        this.$router.push(`/home?citycode=${this.citycode}`)
        this.$notifier.showMessage({ content: '変更が完了しました。', color: 'info' })
      } else {
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '変更できませんでした。', color: 'error' })
        }
      }
    }
  },
}
</script>