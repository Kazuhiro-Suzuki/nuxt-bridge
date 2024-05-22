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
         <v-row>
          <v-col cols="12">
            <v-switch
              v-model="userInfo.get_notification"
              :disabled="disabled"
              dense
              inset
              :color="darkColor"
              label="お知らせ配信時に、プッシュ通知を希望する"
            ></v-switch>
              <v-switch
              v-model="userInfo.is_subscribe"
              :disabled="disabled"
              dense
              inset
              :color="darkColor"
              label="お知らせ配信時に、メール通知を希望する"
            ></v-switch>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <p class="text-left">選択したものを対象としたお知らせを配信します。</p>					
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
              :disabled="disabled"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <!-- <v-text-field
              v-model="userInfo.age"
              label="年齢（数字のみ）"
              :rules="[$rules.isNumber]"
              :disabled="disabled"
              outlined
            ></v-text-field> -->
            <v-autocomplete
              v-model="userInfo.age_range"
              :items="ageOptions"
              item-text="text"
              item-value="value"
              outlined
              clearable
              label="年齢"
              :disabled="disabled"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              v-model="userInfo.address_block"
              :items="addrressOptions"
              outlined
              clearable
              label="お住まいの地名"
              :disabled="disabled"
            ></v-autocomplete>
          </v-col>
        </v-row>
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
      ],

    }
  },
  watch: {
    birthDayMenu (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
  },
  methods: {
    async updateUserInfo() {
      console.log(this.userInfo);
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
  },
  created(){
    console.log("userInfo:", this.userInfo);
    let addressBlockInfo = addressBlock.find(item => item.city_code ==  this.citycode);
    if(addressBlockInfo){
      this.addrressOptions = addressBlockInfo.addrressOptions
    }
  }
}
</script>