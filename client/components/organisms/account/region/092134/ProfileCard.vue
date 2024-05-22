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
        <v-autocomplete
          v-model="userInfo.user_type"
          :items="userTypeChoices"
          outlined
          clearable
          label="本人区分"
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
                label="生年月日"
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
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              v-model="userInfo.notification_tag"
              :items="notificationTopic"
              outlined
              clearable
              multiple
              small-chips
              label="配信を希望するサービス ※任意"
              :disabled="disabled"
              :search-input.sync="search"
              @change="search = ''"
            ></v-autocomplete>
          </v-col>
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
        <v-menu
          ref="expire_date1"
          v-model="expire_date1"
          :close-on-content-click="false"
          :return-value.sync="userInfo.expire_date1"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :disabled="disabled"
                v-model="userInfo.expire_date1"
                label="身体障害者手帳 再認定申請年月 *任意"
                readonly
                outlined
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="userInfo.expire_date1"
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
              @click="$refs.expire_date1.save('')">
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
              @click="$refs.expire_date1.save(userInfo.expire_date1)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
        <v-menu
          ref="expire_date2"
          v-model="expire_date2"
          :close-on-content-click="false"
          :return-value.sync="userInfo.expire_date2"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :disabled="disabled"
                v-model="userInfo.expire_date2"
                label="療育手帳 次回判定時期 *任意"
                readonly
                outlined
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="userInfo.expire_date2"
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
              @click="$refs.expire_date2.save('')">
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
              @click="$refs.expire_date2.save(userInfo.expire_date2)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
        <v-menu
          ref="expire_date3"
          v-model="expire_date3"
          :close-on-content-click="false"
          :return-value.sync="userInfo.expire_date3"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :disabled="disabled"
                v-model="userInfo.expire_date3"
                label="精神障害者保健福祉手帳 有効期限 *任意"
                readonly
                outlined
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="userInfo.expire_date3"
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
              @click="$refs.expire_date3.save('')">
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
              @click="$refs.expire_date3.save(userInfo.expire_date3)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
        <v-menu
          ref="expire_date4"
          v-model="expire_date4"
          :close-on-content-click="false"
          :return-value.sync="userInfo.expire_date4"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :disabled="disabled"
                v-model="userInfo.expire_date4"
                label="自立支援医療（精神通院）受給者証有効期限 *任意"
                readonly
                outlined
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="userInfo.expire_date4"
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
              @click="$refs.expire_date4.save('')">
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
              @click="$refs.expire_date4.save(userInfo.expire_date4)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
        <v-menu
          ref="expire_date5"
          v-model="expire_date5"
          :close-on-content-click="false"
          :return-value.sync="userInfo.expire_date5"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :disabled="disabled"
                v-model="userInfo.expire_date5"
                label="特別児童扶養手当 有効期限 *任意"
                readonly
                outlined
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="userInfo.expire_date5"
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
              @click="$refs.expire_date5.save('')">
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
              @click="$refs.expire_date5.save(userInfo.expire_date5)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
        <v-menu
          ref="expire_date6"
          v-model="expire_date6"
          :close-on-content-click="false"
          :return-value.sync="userInfo.expire_date6"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :disabled="disabled"
                v-model="userInfo.expire_date6"
                label="障害児福祉手当or重度心身障害者手当 有効期限 *任意"
                readonly
                outlined
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="userInfo.expire_date6"
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
              @click="$refs.expire_date6.save('')">
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
              @click="$refs.expire_date6.save(userInfo.expire_date6)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
        <v-menu
          ref="expire_date7"
          v-model="expire_date7"
          :close-on-content-click="false"
          :return-value.sync="userInfo.expire_date7"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :disabled="disabled"
                v-model="userInfo.expire_date7"
                label="特別障害者手当 有効期限 *任意"
                readonly
                outlined
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
          </template>
          <v-date-picker
            v-model="userInfo.expire_date7"
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
              @click="$refs.expire_date7.save('')">
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
              @click="$refs.expire_date7.save(userInfo.expire_date7)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>

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
      search: null,
      formValid: false,
      disabled: true,
      birthDayMenu: false,
      expire_date1: false,
      expire_date2: false,
      expire_date3: false,
      expire_date4: false,
      expire_date5: false,
      expire_date6: false,
      expire_date7: false,
      activePicker: null,
      registerNotification: false,
      registerDisableInfo: false,
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