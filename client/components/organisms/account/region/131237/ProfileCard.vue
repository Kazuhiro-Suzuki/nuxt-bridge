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
          label="障害者との続柄"
          :rules="[$rules.required]"
          :disabled="disabled"
          @change="setUserTypeDetail"
        ></v-autocomplete>
        <div cols="12" v-if="istargetUserType">
          <p class="text-left">障害者との続柄でその他を選択された場合、詳細をご記入ください。</p>
          <TextArea
            :data="userInfo.user_type_detail"
            maxlength="150"
            rows="5"
            label="障害者との続柄がその他の場合の詳細"
            :rules="[$rules.required]"
            :disabled="disabled"
            @textAreaData="setUserTypeDetail"
          />
        </div>
        <v-row>
          <v-col cols="12">
            <v-autocomplete
              v-model="userInfo.disability_type"
              :items="disabilityTypeChoices"
              outlined
              multiple
              clearable
              small-chips
              label="障害の種別等"
              :rules="[$rules.selectArrayRequired]"
              :search-input.sync="search"
              :disabled="disabled"
              @change="search = ''"
            ></v-autocomplete>
          </v-col>
        </v-row>
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
                label="障害者の生年月日"
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
        <p class="text-left">配信を希望するサービスでは、チェックを入れた項目について、個別にお知らせ配信をします。希望するサービスがあれば、チェックを入れてください</p>
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
          <v-col cols="12">
            <v-text-field
            v-model="userInfo.last_name"
            label="氏"
            :disabled="disabled"
            :rules="[$rules.jaFull]"
            outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="userInfo.first_name"
              label="名"
              :disabled="disabled"
              :rules="[$rules.jaFull]"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="userInfo.kana_last_name"
              label="氏（カナ）"
              :disabled="disabled"
              :rules="[$rules.jaFullKana]"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="userInfo.kana_first_name"
              label="名（カナ）"
              :disabled="disabled"
              :rules="[$rules.jaFullKana]"
              outlined
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="userInfo.phone_number"
              outlined
              label="電話番号"
              maxlength="12"
              :disabled="disabled"
              :rules="[$rules.isNumber]"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
                v-model="userInfo.disability_category"
                :items="disabilityCategories"
                label="配慮事項"
                outlined
                clearable
                multiple
                small-chips
                :search-input.sync="search"
                 :disabled="disabled"
                @change="search = ''"
            ></v-autocomplete>
          </v-col>
          <v-col cols="12">
            <TextArea
              :data="userInfo.note1"
              label="障害・病気等の内容"
              maxlength="150"
              rows="5"
              :disabled="disabled"
              @textAreaData="setNote1"
            />
          </v-col> 
          <v-col cols="12">
            <TextArea
              :data="userInfo.note2"
              label="知ってほしいこと（薬、アレルギー、かかりつけ医など）"
              maxlength="150"
              rows="5"
              :disabled="disabled"
              @textAreaData="setNote2"
            />
          </v-col> 
          <v-col cols="12">
            <TextArea
              :data="userInfo.note3"
              label="配慮してほしいこと"
              maxlength="150"
              rows="5"
              :disabled="disabled"
              @textAreaData="setNote3"
            />
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
      activePicker: null,
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
      return this.userInfo.user_type == 'その他'
    },
  },
  watch: {
    birthDayMenu (val) {
      val && setTimeout(() => (this.activePicker = 'YEAR'))
    },
  },
  methods: {
    setUserTypeDetail(value){
      this.userInfo.user_type_detail = value
      if(value != 'その他'){
        this.userInfo.user_type_detail = ''
      }
    },
    setNote1(value){
      this.userInfo.note1 = value
    },
    setNote2(value){
      this.userInfo.note2 = value
    },
    setNote3(value){
      this.userInfo.note3 = value
    },
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
  },
}
</script>