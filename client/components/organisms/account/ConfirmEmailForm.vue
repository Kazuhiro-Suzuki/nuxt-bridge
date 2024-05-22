<template>
  <v-card>
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-card-text>
      <v-form v-model="formValid">
        <v-row>
          <v-col>
            <TextField
              label="メールアドレス"
              maxlength="100"
              icon="mdi-mail"
              :rules="[$rules.required]"
              @textFieldData="setEmail"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-text>
      <NormalButton
        text="変更する"
        :class="`${baseColor} lighten-4`"
        :color="baseColor"
        :disabled="!formValid"
        @clickAction="confirm"
      />
    </v-card-text>
  </v-card>
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
    fullPath: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      data: {
        email: '',
        city_code: '',
      },
      errorMessage: '',
      formValid: false,
    }
  },
  methods: {
    setEmail(value) {
      this.data.email = value
    },
    async confirm() {
      this.data.city_code = this.citycode
      const response = await this.$api.postRequestResetPassword(this.data)
      // console.log(response)
      if (response.status == 200) {
        this.$notifier.showMessage({ content: 'パスワード変更用のURLをメールアドレス宛に送信しました。', color: 'info' })
      } else {
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: 'メールアドレスを確認できませんでした。', color: 'error' })
        }
      }
    },
  },
}
</script>