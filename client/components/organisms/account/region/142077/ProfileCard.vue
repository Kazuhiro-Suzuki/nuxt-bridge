<template>
  <v-card>
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-card-text>
      <v-form v-model="formValid">
        <v-text-field
          v-model="userInfo.email"
          label="メールアドレス"
          disabled
          outlined
        ></v-text-field>
        <v-text-field
          v-model="userInfo.phone_number"
          label="電話番号"
          :disabled="disabled"
          maxlength="12"
          :rules="[$rules.required,$rules.isNumber]"
          outlined
        ></v-text-field>
        <v-text-field
          v-model="userInfo.fax_number"
          label="FAX番号"
          :rules="[$rules.isNumber]"
          :disabled="disabled"
          outlined
        ></v-text-field>
        <v-autocomplete
          v-model="userInfo.user_type"
          :items="userTypeChoices"
          outlined
          clearable
          label="障がい児者との関係"
          :rules="[$rules.required]"
          :disabled="disabled"
        ></v-autocomplete>
        <v-menu
          ref="birthDayMenu"
          v-model="birthDayMenu"
          :close-on-content-click="false"
          :return-value.sync="userInfo.birthday"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :disabled="disabled"
                v-model="userInfo.birthday"
                label="障がい児者の生年月日"
                readonly
                outlined
                v-bind="attrs"
                v-on="on"
                :rules="[$rules.required]"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="userInfo.birthday"
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
              @click="menu = false"
            >
              Cancel
            </v-btn>
            <v-btn
              text
              :color="darkColor"
              @click="$refs.birthDayMenu.save(userInfo.birthday)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
        <v-switch
          v-model="userInfo.get_notification"
          :disabled="disabled"
          dense
          inset
          :color="darkColor"
          :label="`特定の障がい種別ごとに向けたお知らせ配信を希望: ${userInfo.get_notification ? '有効' : '無効'}`"
          @change="setNotificationInfo"
        ></v-switch>
        <v-row v-if="userInfo.get_notification">
          <v-col cols="12">
            <p class="text-left">「本人（家族等）の障がい種別」で選択したものを対象としたお知らせを配信します。</p>					
            <p class="text-left">希望する場合は、以下の項目を入力してください。</p>			    
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="userInfo.disability_type"
              :items="disabilityTypeChoices"
              outlined
              multiple
              clearable
              label="本人（家族等）の障がい種別"
              :rules="[$rules.selectArrayRequired]"
              :disabled="disabled"
            ></v-autocomplete>
          </v-col>
        </v-row>
        <v-switch
          v-model="userInfo.get_disaster_notification"
          :disabled="disabled"
          dense
          inset
          :color="darkColor"
          :label="`災害時のお知らせ配信を希望: ${userInfo.get_disaster_notification ? '有効' : '無効'}`"
          @change="setDisableInfo"
        ></v-switch>
        <v-row  v-if="userInfo.get_disaster_notification">
          <v-col cols="12">
            <p class="text-left">災害発生時の避難所情報等のお知らせを配信します。希望する場合は、以下の項目を入力してください。</p>					
            <p class="text-left">この配信は、「茅ヶ崎市避難行動要支援者支援制度対象要件」を満たしている方のみ利用できます。</p>			    
            <p class="text-left">茅ヶ崎市避難行動要支援者支援制度に登録していない方はこちら<a href="https://www.city.chigasaki.kanagawa.jp/otoshiyori/1023673.html">こちらへ</a></p>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="disabilityCategoryText"
              :items="disabilityCategories"
              label="茅ヶ崎市避難行動要支援者支援制度登録要件"
              outlined
              clearable
              :disabled="disabled"
              :rules="[$rules.required]"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <v-text-field
            v-model="userInfo.last_name"
            label="氏"
            :disabled="disabled"
            :rules="[$rules.required, $rules.jaFull]"
            outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="userInfo.first_name"
              label="名"
              :disabled="disabled"
              :rules="[$rules.required, $rules.jaFull]"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="userInfo.kana_last_name"
              label="氏（カナ）"
              :disabled="disabled"
              :rules="[$rules.required, $rules.jaFullKana]"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="userInfo.kana_first_name"
              label="名（カナ）"
              :disabled="disabled"
              :rules="[$rules.required, $rules.jaFullKana]"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="userInfo.address_block"
              :items="addrressOptions"
              outlined
              clearable
              label="お住まいの地名"
              :disabled="disabled"
              :rules="[$rules.required]"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="userInfo.disablity_number"
              label="手帳番号（数字のみ）"
              :rules="[$rules.required, $rules.isNumber]"
              :disabled="disabled"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
          <v-switch
          v-model="userInfo.is_subscribe"
          :disabled="disabled"
          dense
          inset
          :color="darkColor"
          :label="`メール配信: ${userInfo.is_subscribe ? '有効' : '無効'}`"
        ></v-switch>
      </v-form>
    </v-card-text>
    <v-card-actions class="justify-center">
      <NormalButton
        text="情報を編集する"
        color="grey"
        @clickAction="disabled=!disabled"
      />
      <NormalButton
        text="情報を更新する"
        :class="`${baseColor} lighten-3`"
        :color="baseColor"
        :disabled="(disabled || !formValid)"
        @clickAction="updateUserInfo"
      />
    </v-card-actions>
  </v-card>
</template>

<script>
import { addressBlock } from '../../../../../model/addressBlock'

export default {
  props: {
    title: {
      type: String,
      required: false,
    },
    baseColor: {
      type: String,
      required: false,
    },
    darkColor: {
      type: String,
      required: false,
    },
    citycode: {
      type: String,
      required: true,
    },
    userInfo: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      formValid: false,
      disabled: true,
      birthDayMenu: false,
      activePicker: null,
      registerNotification: false,
      registerDisableInfo: false,
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
        return this.userInfo.disability_category[0] || '';
      },
      set(value){
        this.userInfo.disability_category[0] = value;
      }
    }
  },
  watch: {
    birthDayMenu (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
  },
  methods: {
    async updateUserInfo() {
      let response = await this.$api.putUserInfo(this.userInfo)
      if (response.status == 200) {
        this.disabled = true
        this.$notifier.showMessage({ content: '情報の更新が完了しました。', color: 'info' })
      } else {
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '情報を更新できませんでした。', color: 'error' })
        }

      }
    },
    setNotificationInfo(){
      if(!this.userInfo.get_notification){
        this.userInfo.disability_type = []
        this.userInfo.disablity_grade = ''
      }
    },
    setDisableInfo(){
      if(!this.userInfo.get_disaster_notification){
        this.userInfo.kana_last_name = ''
        this.userInfo.kana_first_name = ''
        this.userInfo.last_name = ''
        this.userInfo.first_name = ''
        this.userInfo.disability_category = []
        this.userInfo.address_block = ''
        this.userInfo.disablity_number = ''
        this.userInfo.disablity_prefecture = ''
      }
      console.log(this.disabled, !this.formValid);
      console.log(this.disabled && !this.formValid);
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