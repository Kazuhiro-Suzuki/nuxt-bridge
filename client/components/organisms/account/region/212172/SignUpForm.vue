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
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              v-model="data.user_type"
              :items="userTypeChoices"
              outlined
              clearable
              label="障がい児者との関係"
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
                    label=" 障がい児者の生年月日 ※任意"
                    readonly
                    outlined
                    v-bind="attrs"
                    v-on="on"
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
            <p class="text-left">選択したものを対象としたお知らせを配信します。</p>					
            <p class="text-left">希望する場合は、以下の項目を入力してください。</p>			    
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="data.disability_type"
              :items="disabilityTypeChoices"
              outlined
              clearable
              multiple
              label="本人（家族等）の障がい種別"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <!-- <TextField
              label="年齢（数字のみ）"
              maxlength="3"
              :rules="[$rules.required,$rules.isNumber]"
              @textFieldData="setAge"
            /> -->
            <v-autocomplete
              v-model="data.age_range"
              :items="ageOptions"
              item-text="text"
              item-value="value"
              outlined
              clearable
              label="年齢"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="data.address_block"
              :items="addrressOptions"
              outlined
              clearable
              label="お住まいの地名"
            ></v-autocomplete>
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
        birthday: '',
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
      addrressOptions:[],
      // addrressOptions: [
      //       "河合",
      //       "宮川",
      //       "古川",
      //       "神岡"
      // ],
      ageOptions: [
        {text: "未就学児", value: "0-5"},
        {text: "小中学生", value: "6-15"},
        {text: "16 - 18歳", value: "16-18"},
        {text: "19 - 29歳", value: "19-29"},
        {text: "30 - 39歳", value: "30-39"},
        {text: "40 - 49歳", value: "40-49"},
        {text: "50 - 59歳", value: "50-59"},
        {text: "60 - 69歳", value: "60-69"},
        {text: "70歳以上", value: "70-200"}
      ],
      disabilityTypeChoices: [
        '身体障害者手帳１級',
        '身体障害者手帳２級',
        '身体障害者手帳３級',
        '身体障害者手帳４級',
        '身体障害者手帳５級',
        '身体障害者手帳６級',
        '療育手帳Ａ１',
        '療育手帳Ａ２',
        '療育手帳Ｂ１',
        '療育手帳Ｂ２',
        '療育手帳Ａ',
        '精神障害者保健福祉手帳１級',
        '精神障害者保健福祉手帳２級',
        '精神障害者保健福祉手帳３級',
        '難病等',
      ],
      userTypeChoices: [
        '本人', 
        '家族', 
        '介助者',
        'その他',
      ]
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