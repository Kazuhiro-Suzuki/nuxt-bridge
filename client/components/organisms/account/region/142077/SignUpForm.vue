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
              <p class="text-left">会員登録は無料です。</p>
              <p class="text-left">会員登録をすると、以下の機能が使えるようになります。</p>
              <p class="text-left">①お知らせ配信通知（お知らせが配信されたとき、登録されたメールアドレスにも通知が届きます。）</p>
              <p class="text-left">②オンライン相談予約</p>
              <p class="text-left">お知らせ、事業所一覧・空き状況、障がい福祉のあんないは、会員登録をしなくても利用できます。</p>
          </v-col>
        </v-row>
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
              label="特定の障がい種別ごとに向けたお知らせ配信を希望"
              @change="setNotificationInfo"
            ></v-checkbox>
          </v-col>
        </v-row>
        <v-row v-if="isDisplayNotificationInfo">
          <v-col cols="12">
            <p class="text-left">「本人（家族等）の障がい種別」で選択したものを対象としたお知らせを配信します。</p>					
            <p class="text-left">希望する場合は、以下の項目を入力してください。</p>			    
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="data.disability_type"
              :items="disabilityTypeChoices"
              outlined
              clearable
              multiple
              :rules="[$rules.selectArrayRequired]"
              label="本人（家族等）の障がい種別"
            ></v-autocomplete>
          </v-col>
        </v-row> 
        <v-row>
          <v-col cols="12">
            <v-checkbox
              v-model="data.get_disaster_notification"
              @change="setDisableInfo"
              label="災害時のお知らせ配信を希望"
            ></v-checkbox>
          </v-col>
        </v-row>
        <v-row v-if="isDisplayDisableInfo">
          <v-col cols="12">
            <p class="text-left">災害発生時の避難所情報等のお知らせを配信します。希望する場合は、以下の項目を入力してください。</p>					
            <p class="text-left">この配信は、「茅ヶ崎市避難行動要支援者支援制度対象要件」を満たしている方のみ利用できます。</p>			    
            <p class="text-left">茅ヶ崎市避難行動要支援者支援制度に登録していない方は<a href="https://www.city.chigasaki.kanagawa.jp/otoshiyori/ikigai/1023673.html">こちらへ</a></p>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
                  v-model="disabilityCategoryText"
                  :items="disabilityCategories"
                  label="茅ヶ崎市避難行動要支援者支援制度登録要件"
                  outlined
                  clearable
                  :rules="[$rules.required]"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12" sm="12" md="12" lg="6" xl="6">
              <TextField
                label="氏"
                :rules="[$rules.required, $rules.jaFull]"
                @textFieldData="setLastName"
              />
            </v-col>
            <v-col cols="12" sm="12" md="12" lg="6" xl="6">
              <TextField
                label="名"
                :rules="[$rules.required, $rules.jaFull]"
                @textFieldData="setFirstName"
              />
            </v-col>
            <v-col cols="12" sm="12" md="12" lg="6" xl="6">
              <TextField
                label="氏（カナ）"
                :rules="[$rules.required, $rules.jaFullKana]"
                @textFieldData="setKanaLastName"
              />
            </v-col>
            <v-col cols="12" sm="12" md="12" lg="6" xl="6">
              <TextField
                label="名（カナ）"
                :rules="[$rules.required, $rules.jaFullKana]"
                @textFieldData="setKanaFirstName"
              />
            </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="data.address_block"
              :items="addrressOptions"
              outlined
              clearable
              label="お住まいの地名"
              :rules="[$rules.required]"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <TextField
              label="手帳番号（数字のみ）"
              maxlength="10"
              :rules="[$rules.required,$rules.isNumber]"
              @textFieldData="setDisablityNumber"
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
        city_code: '',
        type: 'general',
        address_block:'',
        disability_type: [],
        disablity_number: '',
        disability_category: [],
        user_type: '',
        kana_last_name: '',
        kana_first_name: '',
        last_name: '',
        first_name: '',
        birthday: '',
        get_notification: false,
        get_disaster_notification: false,
      },
      passwordShow: false,
      passwordConfirmShow: false,
      birthDayMenu:false,
      activePicker: null,
      errorMessage: '',
      formValid: false,
      isDisplayNotificationInfo: false,
      isDisplayDisableInfo: false,
      addrressOptions:[],
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
        '精神障害者保健福祉手帳１級',
        '精神障害者保健福祉手帳２級',
        '精神障害者保健福祉手帳３級',
        '自立支援医療（精神通院）',
      ],
      userTypeChoices: [
        '本人', 
        '家族', 
        '介助者',
        'その他',
      ],
      disabilityCategories: [
        '上肢の障がい１～２級',
        '下肢の障がい１～３級',
        '体幹機能障害１～３級',
        '視覚障害１～６級',
        '聴覚障害１～６級',
        '知的障がいＡ１～Ａ２',
        'その他の事由'
      ],
    }
  },
  computed: {
    disabilityCategoryText: {
      get(){
        return this.data.disability_category[0] || '';
      },
      set(value){
        this.data.disability_category[0] = value;
      }
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
    setDisablityNumber(value){
      this.data.disablity_number = value
    },
    setNotificationInfo(){
      this.isDisplayNotificationInfo = !this.isDisplayNotificationInfo
      if(!this.isDisplayNotificationInfo){
        this.data.disability_type = []
      }
    },
    setDisableInfo(){
      this.isDisplayDisableInfo = !this.isDisplayDisableInfo
      if(!this.isDisplayDisableInfo){
        this.data.kana_last_name = ''
        this.data.kana_first_name = ''
        this.data.last_name = ''
        this.data.first_name = ''
        this.data.disability_category = []
        this.data.address_block = ''
        this.data.disablity_number = ''
      }
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