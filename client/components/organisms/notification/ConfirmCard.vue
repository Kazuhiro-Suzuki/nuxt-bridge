<template>
  <v-card>
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />

    <v-row>
      <v-col>
        <v-card-text>
          <v-form v-model="formValid">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="data.subject"
                  label="お知らせのタイトル"
                  outlined
                  counter
                  :maxlength="subjectMaxLength"
                  :rules="[$rules.required]"
                  :readonly="readonly"
                  :filled="readonly"
                  background-color="white"
                ></v-text-field>

                <!-- <v-textarea
                  v-model="data.body"
                  label="お知らせの内容"
                  outlined
                  counter
                  rows="10"
                  :maxlength="bodyMaxLength"
                  :rules="[$rules.required]"
                  :readonly="readonly"
                  background-color="white"
                ></v-textarea> -->
                <Viewer
                  ref="viewer"
                  v-if="readonly"
                  :initialValue="data.body"
                />
                <Editor
                  ref="editor"
                  v-if="!readonly"
                  :initialValue="data.body"
                  initialEditType="wysiwyg"
                  :options="editorOptions"
                  height="400px"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <VueCtkDateTimePicker
                  v-model="data.active_since"
                  label="お知らせの通知日時"
                  :minute-interval="15"
                  :format="'YYYY-MM-DD HH:mm'"
                  :overlay="false"
                  locale='ja'
                  :color="baseColor"
                  :disabled="readonly"
                />
              </v-col>
              <v-col cols="12" v-if="is_disaster_info">
                <v-checkbox
                  v-model="data.is_disaster_info"
                  label="災害時のお知らせ"
                  :disabled="readonly"
                ></v-checkbox>
              </v-col>
            </v-row>
            <template v-if="segment_fileds">
              <v-row>
                  <v-col cols="12" sm="12" md="12" lg="12" xl="12">
                      <p class="text-center">セグメント配信の項目を設定してください。</p>
                  </v-col>
              </v-row>
              <v-row justify="center" align="center">
                <v-col v-if="is_segment_birthday" xs="12" sm="12" md="12" lg="5" xl="5">
                  <v-menu
                    v-if="!readonly"
                    ref="birthDayMenu"
                    v-model="birthDayMenu"
                    :close-on-content-click="false"
                    :return-value.sync="data.segment_birthday"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                  >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model="data.segment_birthday"
                          label="誕生年月"
                          prepend-inner-icon="mdi-calendar"
                          readonly
                          outlined
                          v-bind="attrs"
                          v-on="on"
                        ></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="data.segment_birthday"
                      type="month"
                      :color="baseColor"
                      no-title
                      scrollable
                      locale="ja"
                      header-color="primary"
                    >
                      <v-spacer></v-spacer>
                      <v-btn 
                        text 
                        :color="baseColor" 
                        @click="$refs.birthDayMenu.save('')">
                        クリア
                      </v-btn>
                      <v-btn
                        text
                        :color="baseColor"
                        @click="birthDayMenu = false"
                      >
                        キャンセル
                      </v-btn>
                      <v-btn
                        text
                        :color="baseColor"
                        @click="$refs.birthDayMenu.save(data.segment_birthday)"
                      >
                        OK
                      </v-btn>
                    </v-date-picker>
                  </v-menu>
                  <v-text-field
                    v-else
                    v-model="data.segment_birthday"
                    label="誕生年月"
                    outlined
                    :readonly="readonly"
                    :filled="readonly"
                    background-color="white"
                  ></v-text-field>
                </v-col>
                <v-col v-if="is_segment_birthday_year" cols="12" sm="12" md="12" lg="5" xl="5">
                    <v-autocomplete
                      v-if="!readonly"
                      v-model="data.segment_birthday_year"
                      :items="yearOptions"
                      outlined
                      multiple
                      label="誕生年"
                    ></v-autocomplete>
                    <v-text-field
                      v-else
                      v-model="formattedBirthdayYear"
                      label="誕生年"
                      outlined
                      :readonly="readonly"
                      :filled="readonly"
                      background-color="white"
                    ></v-text-field>
                </v-col>
                <v-col v-if="is_segment_birthday_month" cols="12" sm="12" md="12" lg="5" xl="5">
                    <v-autocomplete
                      v-if="!readonly"
                      v-model="data.segment_birthday_month"
                      :items="monthOptions"
                      outlined
                      multiple
                      label="誕生月"
                    ></v-autocomplete>
                    <v-text-field
                      v-else
                      v-model="formattedBirthdayMonth"
                      label="誕生月"
                      outlined
                      :readonly="readonly"
                      :filled="readonly"
                      background-color="white"
                    ></v-text-field>
                </v-col>
                <v-col v-if="ageOptions.length !== 0" xs="12" sm="12" md="5" lg="5">
                  <v-autocomplete
                      v-if="!readonly"
                      clearable
                      v-model="data.segment_age_range"
                      :items="ageOptions"
                      item-name="text"
                      item-value="value"
                      outlined
                      multiple
                      label="年齢"
                    ></v-autocomplete>
                    <v-text-field
                      v-else
                      v-model="formattedAgeRange"
                      label="年齢"
                      outlined
                      :readonly="readonly"
                      :filled="readonly"
                      background-color="white"
                    ></v-text-field>
                </v-col>
                <v-col v-if="addrressOptions.length !== 0" xs="12" sm="12" md="5" lg="5">
                  <v-autocomplete
                      v-if="!readonly"
                      clearable
                      v-model="data.segment_address_block"
                      :items="addrressOptions"
                      outlined
                      multiple
                      label="お住まいの地名"
                    ></v-autocomplete>
                    <v-text-field
                      v-else
                      v-model="data.segment_address_block"
                      label="お住まいの地名"
                      outlined
                      :readonly="readonly"
                      :filled="readonly"
                      background-color="white"
                    ></v-text-field>
                </v-col>
                <v-col v-if="userTypeChoices.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5">
                    <v-autocomplete
                      v-if="!readonly"
                      v-model="data.segment_user_type"
                      :items="userTypeChoices"
                      outlined
                      multiple
                      label="障害児者との関係"
                    ></v-autocomplete>
                    <v-text-field
                      v-else
                      v-model="data.segment_user_type"
                      label="障害児者との関係"
                      outlined
                      :readonly="readonly"
                      :filled="readonly"
                      background-color="white"
                    ></v-text-field>
                  </v-col>
                  <v-col v-if="disabilityTypeChoices.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5">
                    <v-autocomplete
                      v-if="!readonly"
                      v-model="data.segment_disability_type"
                      :items="disabilityTypeChoices"
                      outlined
                      multiple
                      label="本人（家族等）の障害種別"
                    ></v-autocomplete>
                    <v-text-field
                      v-else
                      v-model="data.segment_disability_type"
                      label="本人（家族等）の障害種別"
                      outlined
                      :readonly="readonly"
                      :filled="readonly"
                      background-color="white"
                    ></v-text-field>
                  </v-col>
                  <v-col v-if="notificationTags.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5">
                    <v-autocomplete
                      v-if="!readonly"
                      v-model="data.segment_notification_tag"
                      :items="notificationTags"
                      outlined
                      multiple
                      label="配信に関連したサービス"
                    ></v-autocomplete>
                    <v-text-field
                      v-else
                      v-model="data.segment_notification_tag"
                      label="配信に関連したサービス"
                      outlined
                      :readonly="readonly"
                      :filled="readonly"
                      background-color="white"
                    ></v-text-field>
                  </v-col>
                  <v-col v-if="notificationCategories.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5">
                    <v-autocomplete
                      v-if="!readonly"
                      v-model="data.segment_notification_category"
                      :items="notificationCategories"
                      item-value="text"
                      outlined
                      multiple
                      label="お知らせのカテゴリ"
                    ></v-autocomplete>
                    <v-text-field
                      v-else
                      v-model="data.segment_notification_category"
                      label="お知らせのカテゴリ"
                      outlined
                      :readonly="readonly"
                      :filled="readonly"
                      background-color="white"
                    ></v-text-field>
                  </v-col>
              </v-row>
            </template>
          </v-form>
        </v-card-text>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <div>
      <v-card-actions
        class="justify-center"
      >
        <div v-if="buttonText=='閉じる'">
          <TextButton
            :text="buttonText"
            :color="darkColor"
            @clickEvent1="$emit('clickEvent3')"
          />
        </div>
        <div v-else>
          <TextButton
            :text="buttonText"
            :color="darkColor"
            :disabled="!formValid"
            @clickEvent1="dialog = !dialog"
          />
        </div>
      </v-card-actions>
    </div>

    <v-dialog
      v-model="dialog"
      :width="dialogWidth"
    >
      <Confirmation
        v-if="regionData.city_code == '131032'"
        title="確認"
        :baseColor="baseColor"
        :darkColor="darkColor"
        buttonText="確定する"
        @clickEvent2="clickEvent2Method"
      />
       <Confirmation
        v-else
        :isNormalButton="true"
        :btnClass="btnClass"
        :title="confirmTitle"
        :baseColor="baseColor"
        :darkColor="darkColor"
        :buttonText="confirmButtonText"
        @clickAction1="clickEvent2Method"
      >
        <template v-slot:userInfo>
          <slot name="confirmText"></slot>
        </template>
        <template v-slot:firstAction>
          <slot name="firstAction"></slot>
        </template>
      </Confirmation>
    </v-dialog>

  </v-card>
</template>

<script>
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker'
import { Viewer, Editor } from '@toast-ui/vue-editor'
import { mapGetters } from 'vuex'
import { notificationField } from '@/model/NotificationField'

export default {
  components: {
    VueCtkDateTimePicker,
    Viewer,
    Editor
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    confirmTitle: {
      type: String,
      required: false,
    },
    confirmButtonText: {
      type: String,
      required: false,
    },
    baseColor: {
      type: String,
      required: true,
    },
    darkColor: {
      type: String,
      required: true,
    },
    data: {
      type: Object,
      required: true
    },
    buttonText: {
      type: String,
      required: false,
    },
    readonly: {
      type: Boolean,
      required: false,
    },
    subjectMaxLength: {
      type: String,
      required: true,
    },
    bodyMaxLength: {
      type: String,
      required: true,
    },
    btnClass: {
      type: String,
      required: false,
    }
  },
  data() {
    return {
      dialog: false,
      dialogWidth: '400',
      formValid: false,
      fileIds: [],
      editorOptions: {
        initialEditType: 'wysiwyg',
        placeholder: 'お知らせの内容',
        language: 'ja',
        hooks: {
          addImageBlobHook: this.addImageBlobHook,
        },
      },
      birthDayMenu:false,
      is_disaster_info: false,
      is_segment_birthday: false,
      is_segment_birthday_year: false,
      is_segment_birthday_month: false,
      disabilityTypeChoices: [],
      userTypeChoices: [],
      addrressOptions:[],
      ageOptions: [],
      monthOptions: [
        {text: "1月", value: "0000-01"},
        {text: "2月", value: "0000-02"},
        {text: "3月", value: "0000-03"},
        {text: "4月", value: "0000-04"},
        {text: "5月", value: "0000-05"},
        {text: "6月", value: "0000-06"},
        {text: "7月", value: "0000-07"},
        {text: "8月", value: "0000-08"},
        {text: "9月", value: "0000-09"},
        {text: "10月", value: "0000-10"},
        {text: "11月", value: "0000-11"},
        {text: "12月", value: "0000-12"},
      ],
      yearOptions: [],
      notificationTags: [],
      notificationCategories: [],
      segment_fileds: false,
    }
  },
  methods: {
    clickEvent2Method() {
      if(!this.readonly){
        const extractedMarkdown = this.$refs.editor.invoke('getMarkdown')
        this.data.body = extractedMarkdown
        this.data.file_ids = this.fileIds
      }
      if(this.data.segment_birthday_month.length != 0){
        this.data.segment_birthday_month.sort()
      }
      if(this.is_segment_birthday){
        if(this.data.segment_birthday != '' && this.data.segment_birthday_month.length !== 0){
          this.$notifier.showMessage({ content: '誕生年月と誕生月はどちらか１つを指定してください。', color: 'error' })
            return false
        }
      }
      this.dialog = false
      this.$emit('clickEvent3')
    },
    async addImageBlobHook(blob, addImageCallback) {
      this.$emit('openDialog', true)
      const description = document.getElementById('toastuiAltTextInput')?.value
      const formData = new FormData()
      formData.append('files', blob)
      formData.append('city_code', this.regionData.city_code)
      formData.append('visible_scope', 'public')

      const config = {
        headers: {
          'content-type': 'multipart/form-data'
        },
      }
  
      const response = await this.$api.uploadAssets(formData, config)
      if (response.data.uploaded_files.length > 0) {
        let file_id = response.data.uploaded_files[0].id
        this.fileIds.push(file_id)
        addImageCallback(
          '/api/v1/app/upload_file/public/?file_id=' + file_id,
          description || response.data.uploaded_files[0].file_name
        )
      }
      this.$emit('openDialog', false)
    },
    populateYears() {
      const currentYear = new Date().getFullYear();
      const startYear = currentYear - 100; // You can adjust the range as needed

      for (let year = startYear; year <= currentYear; year++) {
        this.yearOptions.push(year.toString());
      }
    },
  },
  mounted() {
    this.populateYears();
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    }),
    formattedBirthdayMonth() {
      if(this.data.segment_birthday_month.length == 0){
        return;
      }
      const formattedMonths = this.data.segment_birthday_month.map((value) => {
        const matchingOption = this.monthOptions.find((option) => option.value === value);
        return matchingOption.text;
      });

      return formattedMonths.join(', ');
    },
    formattedBirthdayYear() {
      if(this.data.segment_birthday_year.length == 0){
        return;
      }
      const formattedYears = this.data.segment_birthday_year.map((value) => {
        const matchingOption = this.yearOptions.find((option) => option === value);
        return matchingOption;
      });

      return formattedYears.join(', ');
    },
    formattedAgeRange() {
      if(this.data.segment_age_range.length == 0){
        return;
      }
      const formattedAgeRange = this.data.segment_age_range.map((value) => {
        const matchingOption = this.ageOptions.find((option) => option.value === value);
        return matchingOption.text;
      });

      return formattedAgeRange.join(', ');
    }
  },
  created(){
    let notificationInfo = notificationField.find(item => item.city_code ==  this.regionData.city_code);
    this.segment_fileds  = notificationInfo.segment_fileds
    this.is_segment_birthday = notificationInfo.is_segment_birthday
    this.is_segment_birthday_year = notificationInfo.is_segment_birthday_year
    this.is_segment_birthday_month = notificationInfo.is_segment_birthday_month
    this.is_disaster_info = notificationInfo.is_disaster_info
    if(!this.segment_fileds){
      return
    }
    if(notificationInfo.addrressOptions !== undefined){
      this.addrressOptions = notificationInfo.addrressOptions
    }
    if(notificationInfo.ageOptions !== undefined){
      this.ageOptions = notificationInfo.ageOptions
    }
    if(notificationInfo.userTypeChoices !== undefined){
      this.userTypeChoices = notificationInfo.userTypeChoices
    }
    if(notificationInfo.disabilityTypeChoices !== undefined){
      this.disabilityTypeChoices = notificationInfo.disabilityTypeChoices
    }
    if(notificationInfo.notificationTags !== undefined){
      this.notificationTags = notificationInfo.notificationTags
    }
    if(notificationInfo.notificationCategories !== undefined){
      this.notificationCategories = notificationInfo.notificationCategories
    }
  }
}
</script>