<template>
  <v-card>
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-card-text>
      <v-form v-model="formValid">
        <v-row>
          <v-col cols="12">
            <TextField
              label="メールアドレス"
              maxlength="100"
              icon="mdi-mail"
              :rules="[$rules.required]"
              @textFieldData="setEmail"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p class="text-left">パスワードは、半角数字及び大文字小文字の半角英字を含む8文字以上50文字以下で入力してください</p>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
            <TextField
              label="パスワード"
              maxlength="50"
              icon="mdi-lock"
              :append-icon="passwordShow ? 'mdi-eye' : 'mdi-eye-off'"
              :type="passwordShow ? 'text' : 'password'"
              @clickAction="passwordShow = !passwordShow"
              :rules="[$rules.required]"
              @textFieldData="setPassword"
            />
          </v-col>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
            <TextField
              label="パスワード再確認"
              maxlength="50"
              icon="mdi-lock"
              :append-icon="passwordConfirmShow ? 'mdi-eye' : 'mdi-eye-off'"
              :type="passwordConfirmShow ? 'text' : 'password'"
              @clickAction="passwordConfirmShow = !passwordConfirmShow"
              :rules="[$rules.required]"
              @textFieldData="setPasswordReconfirm"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
            <TextField
              label="電話番号（数字のみ）"
              maxlength="12"
              icon="mdi-phone"
              :rules="[$rules.required,$rules.isNumber]"
              @textFieldData="setPhoneNumber"
            />
          </v-col>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
            <TextField
              label="FAX番号（数字のみ）※任意"
              maxlength="12"
              icon="mdi-fax"
              :rules="[$rules.isNumber]"
              @textFieldData="setFaxNumber"
            />
          </v-col>
        </v-row>
        
      </v-form>
      <p class="text-left">
        「登録する」ボタンを押下し、登録が完了すると入力されたメールアドレス宛にメールが送信されますので、そちらに記載されたURLにアクセスしてください。
      </p>
    </v-card-text>
    <v-card-text>
      <NormalButton
        text="登録する"
        class="`${baseColor} lighten-4`"
        :color="baseColor"
        :disabled="!formValid"
        @clickAction="signUp"
      />
    </v-card-text>
  </v-card>
</template>

<script>
import SelectBox from '../../../../atoms/inputs/SelectBox.vue'


export default {
  components: { SelectBox },
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
    darkColor: {
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
        password_reconfirm: '',
        phone_number: '',
        fax_number: '',
        city_code: '',
        type: 'general',
        get_notification: true,
        get_disaster_notification: true,
      },
      passwordShow: false,
      passwordConfirmShow: false,
      errorMessage: '',
      formValid: false,
    }
  },
  methods: {
    setEmail(value) {
      this.data.email = value
    },
    setPassword(value) {
      this.data.password = value
    },
    setPasswordReconfirm(value) {
      this.data.password_reconfirm = value
    },
    setPhoneNumber(value) {
      this.data.phone_number = value
    },
    setFaxNumber(value) {
      this.data.fax_number = value
    },
    async signUp() {
      this.data.city_code = this.citycode
      // console.log(this.data);
      const response = await this.$api.postSignUpInfo(this.data)
      // console.log(response)
      if (response.status == 201) {
        this.$notifier.showMessage({ content: '登録されたメールアドレス宛にメールを送信しました。', color: 'info' })
        this.$router.push(`/home?citycode=${this.citycode}`)
      } else {
        if (response.data.detail) {
          this.$emit('errorEvent', response.data.detail)
          window.scrollTo({
            top: 0,
            behavior: 'smooth',
          })
        } else {
          this.$emit('errorEvent', '会員登録できません、入力情報を確認してください。')
        }
      }
    },
  },
}
</script>