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
              icon="mdi-mail"
              :rules="[$rules.required]"
              @textFieldData="setEmail"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <div class="text-left">パスワードは、半角数字及び大文字小文字の半角英字を含む8文字以上50文字以下で入力してください</div>
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
          <v-col cols="12">
            <v-autocomplete
              v-model="data.user_type"
              :items="userTypeChoices"
              outlined
              clearable
              label="障害者との続柄"
              :rules="[$rules.required]"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" v-if="istargetUserType">
            <p class="text-left">障害者との続柄でその他を選択された場合、詳細をご記入ください。</p>
            <TextArea
              maxlength="150"
              rows="5"
              label="障害者との続柄がその他の場合の詳細"
              :rules="[$rules.required]"
              @textAreaData="setUserTypeDetail"
            />
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="data.disability_type"
              :items="disabilityTypeChoices"
              outlined
              clearable
              multiple
              small-chips
              :rules="[$rules.selectArrayRequired]"
              label="障害の種別等"
              :search-input.sync="search"
              @change="search = ''"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <v-menu
              ref="birthDayMenu"
              v-model="birthDayMenu"
              :close-on-content-click="false"
              :return-value.sync="data.birthday"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="data.birthday"
                    label="障害者の生年月日"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
                    :rules="[$rules.required]"
                  ></v-text-field>
              </template>
              <v-date-picker
                v-model="data.birthday"
                no-title
                scrollable
                :color="darkColor"
                locale="ja"
                :active-picker.sync="activePicker"
                :max="(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)"
              >
                <v-spacer></v-spacer>
                <v-btn 
                  text 
                  :color="darkColor" 
                  @click="$refs.birthDayMenu.save('')">
                  クリア
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="birthDayMenu = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="$refs.birthDayMenu.save(data.birthday)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>  
          </v-col>
          <v-col cols="12">
            <div class="text-left">配信を希望するサービスでは、チェックを入れた項目について、個別にお知らせ配信をします。希望するサービスがあれば、チェックを入れてください</div>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="data.notification_tag"
              :items="notificationTopic"
              outlined
              clearable
              multiple
              small-chips
              label="配信を希望するサービス ※任意"
              :search-input.sync="search"
              @change="search = ''"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <v-checkbox
              v-model="data.get_notification"
              label="お知らせ配信時に、プッシュ通知を希望する"
            ></v-checkbox>
            <v-checkbox
              v-model="data.is_subscribe"
              label="お知らせ配信時に、メール通知を希望する"
            ></v-checkbox>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <DenseToolBar
              title="ヘルプカードの作成"
              :baseColor="baseColor"
            />
          </v-col>
          <v-col>
            <div class="text-left">ヘルプカードの作成をご希望の場合は下記の任意項目の設定をしてください。</div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
            <TextField
              label="氏"
              @textFieldData="setLastName"
            />
          </v-col>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
            <TextField
              label="名"
              @textFieldData="setFirstName"
            />
          </v-col>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
            <TextField
              label="氏（カナ）"
              @textFieldData="setKanaLastName"
            />
          </v-col>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
            <TextField
              label="名（カナ）"
              @textFieldData="setKanaFirstName"
            />
          </v-col>
          <v-col cols="12">
            <TextField
              label="電話番号（数字のみ）"
              maxlength="12"
              icon="mdi-phone"
              @textFieldData="setPhoneNumber"
            />
          </v-col>
          <v-col cols="12">
            <v-autocomplete
                v-model="data.disability_category"
                :items="disabilityCategories"
                label="配慮事項"
                outlined
                clearable
                multiple
                small-chips
                :search-input.sync="search"
                @change="search = ''"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <TextArea
              label="障害・病気等の内容"
              maxlength="150"
              rows="5"
              @textAreaData="setNote1"
            />
          </v-col> 
          <v-col cols="12">
            <TextArea
              label="知ってほしいこと（薬、アレルギー、かかりつけ医など）"
              maxlength="150"
              rows="5"
              @textAreaData="setNote2"
            />
          </v-col> 
          <v-col cols="12">
            <TextArea
              label="配慮してほしいこと"
              maxlength="150"
              rows="5"
              @textAreaData="setNote3"
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
      search: null,
      data: {
        email: '',
        password: '',
        password_reconfirm: '',
        phone_number: '',
        fax_number: '',
        city_code: '',
        type: 'general',
        address_block:'',
        disability_type: [],
        disability_category: [],
        user_type: '',
        user_type_detail: '',
        kana_last_name: '',
        kana_first_name: '',
        last_name: '',
        first_name: '',
        birthday: '',
        notification_tag: [],
        note1: '',
        note2: '',
        note3: '',
        is_func1: '',
        get_notification: true,
        is_subscribe: true,
        get_disaster_notification: true,
      },
      passwordShow: false,
      passwordConfirmShow: false,
      birthDayMenu:false,
      activePicker: null,
      errorMessage: '',
      formValid: false,
      // createHelpCard: false,
      disabilityTypeChoices: [
        '身体障害',
        '知的障害',
        '精神障害',
        '難病',
        '医療的ケア児',
      ],
      userTypeChoices: [
        '本人',
        '家族',
        'その他',
      ],
      notificationTopic: [
        'ストマ装具（日常生活用具おむつを含む）',
        '福祉タクシー券',
        '都営交通無料乗車券',
        '有料道路割引'
      ],
      disabilityCategories: [
        '目が不自由です。',
        '足が不自由です。',
        '耳が不自由です。',
        '手が不自由です。',
        'コミュニケーションが苦手です。',
        '移動のときに誘導してください。',
        '手話か筆談などで伝えてください。',
        'パニックになることがあります。',
        '人工透析をしています。',
        '発作があります。'
      ],
    }
  },
  computed: {
    istargetUserType(){
      if(this.data.user_type == 'その他'){
        return true
      }
      this.data.user_type_detail = ''
      return false
    }
  },
  watch: {
    birthDayMenu (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
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
    setLastName(value){
      this.data.last_name = value
    },
    setFirstName(value){
      this.data.first_name = value
    },
    setKanaLastName(value){
      this.data.kana_last_name = value
    },
    setKanaFirstName(value){
      this.data.kana_first_name = value
    },
    setUserTypeDetail(value){
      this.data.user_type_detail = value
    },
    setNote1(value){
      console.log(value);
      this.data.note1 = value
    },
    setNote2(value){
      this.data.note2 = value
    },
    setNote3(value){
      this.data.note3 = value
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