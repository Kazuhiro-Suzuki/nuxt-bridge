<template>
  <v-card>
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-card-text>
      <v-form v-model="formValid">
        <TextField
          label="メールアドレス"
          :maxlength="emailMaxLength"
          icon="mdi-mail"
          :rules="[$rules.required]"
          @textFieldData="setEmail"
        />
        <TextField
          label="パスワード"
          :maxlength="passwordMaxLength"
          icon="mdi-lock"
          :append-icon="passwordShow ? 'mdi-eye' : 'mdi-eye-off'"
          :type="passwordShow ? 'text' : 'password'"
          @clickAction="passwordShow = !passwordShow"
          :rules="[$rules.required]"
          @textFieldData="setPassword"
        />
        <NormalButton
          text="ログイン"
          :class="`${baseColor} lighten-4`"
          :color="baseColor"
          icon="mdi-login"
          :disabled="!formValid"
          @clickAction="login"
        />
      </v-form>
    </v-card-text>
    <v-card-text>
      <v-row justify="center">
        <LinkButton
          text="新規会員登録の方はこちら"
          color="blue"
          :path="pathTermOfService"
        />
      </v-row>
      <v-row justify="center">
        <LinkButton
          text="パスワードを忘れた方はこちら"
          color="black"
          :path="pathResetPassword"
        />
      </v-row>
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
        password: '',
        city_code: '',
      },
      passwordShow: false,
      emailMaxLength: '100',
      passwordMaxLength: '100',
      errorMessage: '',
      formValid: false,
      isAdminPath: false,
      pathTermOfService: '',
      pathResetPassword: '',
    }
  },
  methods: {
    setEmail(value) {
      this.data.email = value
    },
    setPassword(value) {
      this.data.password = value
    },
    login() {
      this.data.city_code = this.citycode
      this.$auth
        .loginWith('refresh', { data: this.data })
        .then((res) => {
          // console.log(res)
          console.log("$redirect_url", this.$route);
          if(this.$route.query.redirect_uri){
            console.log("redirect_url");
            console.log(this.$route.query.redirect_uri);
            console.log(decodeURIComponent(this.$route.query.redirect_uri));
            this.$router.push(decodeURIComponent(this.$route.query.redirect_uri))
            return;
          }
          console.log("$redirect", this.$route);
          if(this.$route.query.redirect){
            console.log('redirect');
            console.log('URL:',this.$route.query.redirect);
            console.log('URL:',decodeURIComponent(this.$route.query.redirect));
            let jwtToken = this.$auth.strategy.token.get().split(' ');
            let token = jwtToken[1]
            window.location.href = decodeURIComponent(this.$route.query.redirect) + '?token=' + token
            return;
          }
          console.log("$home", this.$route);
          this.$router.push(`/home?citycode=${this.citycode}`)
          this.$notifier.showMessage({ content: 'ログインしました。', color: 'info' })
        })
        .catch((err) => {
          if (err.response.data.detail) {
            this.$notifier.showMessage({ content: err.response.data.detail, color: 'error' })
          } else {
            this.$notifier.showMessage({ content: 'ログインできません。', color: 'error' })
          }
        })
    }
  },
  created() {
    this.pathTermOfService = `/account/termofservice?citycode=${this.citycode}`
    if (this.fullPath.match('admin')) {
      this.isAdminPath = true
      this.pathResetPassword = `/admin/account/confirmemail?citycode=${this.citycode}`
    } else {
      this.pathResetPassword = `/account/confirmemail?citycode=${this.citycode}`
    }
  },
}
</script>