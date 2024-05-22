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
          <v-col cols="12">
            <v-autocomplete
              v-model="data.user_type"
              :items="userTypeChoices"
              outlined
              clearable
              label="本人区分"
              :rules="[$rules.required]"
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
                    label="生年月日"
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
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              v-model="data.address_block"
              :items="addrressOptions"
              outlined
              clearable
              label="地域（居住地区）"
              :rules="[$rules.required]"
            ></v-autocomplete>
          </v-col>
        </v-row>
        <v-row>
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
            <v-menu
              ref="expire_date1"
              v-model="expire_date1"
              :close-on-content-click="false"
              :return-value.sync="data.expire_date1"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="data.expire_date1"
                    label="身体障害者手帳 再認定申請年月 ※任意"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
              </template>
              <v-date-picker
                v-model="data.expire_date1"
                no-title
                scrollable
                :color="darkColor"
                locale="ja"
                :active-picker.sync="activePicker"
                :min="min6year"
                :max="max6year"
              >
                <v-spacer></v-spacer>
                <v-btn 
                  text 
                  :color="darkColor" 
                  @click="$refs.expire_date1.save('')">
                  クリア
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="expire_date1 = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="$refs.expire_date1.save(data.expire_date1)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>  
          </v-col>
          <v-col cols="12">
            <v-menu
              ref="expire_date2"
              v-model="expire_date2"
              :close-on-content-click="false"
              :return-value.sync="data.expire_date2"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="data.expire_date2"
                    label="療育手帳 次回判定時期 ※任意"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
              </template>
              <v-date-picker
                v-model="data.expire_date2"
                no-title
                scrollable
                :color="darkColor"
                locale="ja"
                :active-picker.sync="activePicker"
                :min="min6year"
                :max="max6year"
              >
                <v-spacer></v-spacer>
                <v-btn 
                  text 
                  :color="darkColor" 
                  @click="$refs.expire_date2.save('')">
                  クリア
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="expire_date2 = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="$refs.expire_date2.save(data.expire_date2)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>  
          </v-col>
          <v-col cols="12">
            <v-menu
              ref="expire_date3"
              v-model="expire_date3"
              :close-on-content-click="false"
              :return-value.sync="data.expire_date3"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="data.expire_date3"
                    label="精神障害者保健福祉手帳 有効期限 ※任意"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
              </template>
              <v-date-picker
                v-model="data.expire_date3"
                no-title
                scrollable
                :color="darkColor"
                locale="ja"
                :active-picker.sync="activePicker"
                :min="min6year"
                :max="max6year"
              >
                <v-spacer></v-spacer>
                <v-btn 
                  text 
                  :color="darkColor" 
                  @click="$refs.expire_date3.save('')">
                  クリア
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="expire_date3 = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="$refs.expire_date3.save(data.expire_date3)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>  
          </v-col>
          <v-col cols="12">
            <v-menu
              ref="expire_date4"
              v-model="expire_date4"
              :close-on-content-click="false"
              :return-value.sync="data.expire_date4"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="data.expire_date4"
                    label="自立支援医療（精神通院）受給者証有効期限 ※任意"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
              </template>
              <v-date-picker
                v-model="data.expire_date4"
                no-title
                scrollable
                :color="darkColor"
                locale="ja"
                :active-picker.sync="activePicker"
                :min="min6year"
                :max="max6year"
              >
                <v-spacer></v-spacer>
                <v-btn 
                  text 
                  :color="darkColor" 
                  @click="$refs.expire_date4.save('')">
                  クリア
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="expire_date4 = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="$refs.expire_date4.save(data.expire_date4)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>  
          </v-col>
          <v-col cols="12">
            <v-menu
              ref="expire_date5"
              v-model="expire_date5"
              :close-on-content-click="false"
              :return-value.sync="data.expire_date5"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="data.expire_date5"
                    label="特別児童扶養手当 有効期限 ※任意"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
              </template>
              <v-date-picker
                v-model="data.expire_date5"
                no-title
                scrollable
                :color="darkColor"
                locale="ja"
                :active-picker.sync="activePicker"
                :min="min6year"
                :max="max6year"
              >
                <v-spacer></v-spacer>
                <v-btn 
                  text 
                  :color="darkColor" 
                  @click="$refs.expire_date5.save('')">
                  クリア
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="expire_date5 = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="$refs.expire_date5.save(data.expire_date5)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>  
          </v-col>
          <v-col cols="12">
            <v-menu
              ref="expire_date6"
              v-model="expire_date6"
              :close-on-content-click="false"
              :return-value.sync="data.expire_date6"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="data.expire_date6"
                    label="障害児福祉手当 or 重度心身障害者手当 有効期限 ※任意"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
              </template>
              <v-date-picker
                v-model="data.expire_date6"
                no-title
                scrollable
                :color="darkColor"
                locale="ja"
                :active-picker.sync="activePicker"
                :min="min6year"
                :max="max6year"
              >
                <v-spacer></v-spacer>
                <v-btn 
                  text 
                  :color="darkColor" 
                  @click="$refs.expire_date6.save('')">
                  クリア
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="expire_date6 = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="$refs.expire_date6.save(data.expire_date6)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>  
          </v-col>
          <v-col cols="12">
            <v-menu
              ref="expire_date7"
              v-model="expire_date7"
              :close-on-content-click="false"
              :return-value.sync="data.expire_date7"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="data.expire_date7"
                    label="特別障害者手当 有効期限 ※任意"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
              </template>
              <v-date-picker
                v-model="data.expire_date7"
                no-title
                scrollable
                :color="darkColor"
                locale="ja"
                :active-picker.sync="activePicker"
                :min="min6year"
                :max="max6year"
              >
                <v-spacer></v-spacer>
                <v-btn 
                  text 
                  :color="darkColor" 
                  @click="$refs.expire_date7.save('')">
                  クリア
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="expire_date7 = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  :color="darkColor"
                  @click="$refs.expire_date7.save(data.expire_date7)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>  
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
import { addressBlock } from '../../../../../model/addressBlock'


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
        age: '',
        age_range:'',
        city_code: '',
        type: 'general',
        address_block:'',
        disability_type: [],
        disablity_number: '',
        // disability_category: [],
        user_type: '',
        kana_last_name: '',
        kana_first_name: '',
        last_name: '',
        first_name: '',
        notification_tag: [],
        birthday: '',
        expire_date1: '',
        expire_date2: '',
        expire_date3: '',
        expire_date4: '',
        expire_date5: '',
        expire_date6: '',
        expire_date7: '',
        get_notification: true,
        is_subscribe: true,
        get_disaster_notification: true,
      },
      passwordShow: false,
      passwordConfirmShow: false,
      birthDayMenu:false,
      expire_date1: false,
      expire_date2: false,
      expire_date3: false,
      expire_date4: false,
      expire_date5: false,
      expire_date6: false,
      expire_date7: false,
      activePicker: null,
      errorMessage: '',
      formValid: false,
      addrressOptions:[],
      userTypeChoices: [
        '本人', 
        '家族（介助者）', 
        '事業所',
        'その他',
      ],
      notificationTopic: [
        '精神障害者保健福祉手帳',
        '自立支援医療（精神通院）',
        '日常生活用具（ストマ・おむつ）',
        '子育て（発達支援・療育）'
      ]
    }
  },
  computed: {
    min6year(){
      let today = new Date(); // 現在の日付を取得
      let sixYearsAgo = new Date(today.getFullYear() - 6, today.getMonth(), today.getDate()); // 現在の日付から6年前の日付を計算
      let minDate = sixYearsAgo.toISOString(); // ISO形式に変換
      return minDate;
    },
    max6year(){
      let today = new Date(); // 現在の日付を取得
      let sixYears = new Date(today.getFullYear() + 6, today.getMonth(), today.getDate()); // 現在の日付から6年前の日付を計算
      let maxDate = sixYears.toISOString() // ISO形式に変換
      return maxDate;
    }
  },
  watch: {
    birthDayMenu (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
    expire_date1 (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
    expire_date2 (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
    expire_date3 (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
    expire_date4 (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
    expire_date5 (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
    expire_date6 (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
    expire_date7 (val) {
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
    setFaxNumber(value) {
      this.data.fax_number = value
    },
    // setAge(value){
    //   this.data.age = value
    // },
    setNotificationInfo(){
        this.data.disability_type = []
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
        } else {
          this.$emit('errorEvent', '会員登録できません、入力情報を確認してください。')
        }
        window.scrollTo({
          top: 0,
          behavior: 'smooth',
        })
      }
    },
  },
  created(){
    let addressBlockInfo = addressBlock.find(item => item.city_code ==  this.citycode);
    if(addressBlockInfo){
      this.addrressOptions = addressBlockInfo.addrressOptions
    }
  }
}
</script>