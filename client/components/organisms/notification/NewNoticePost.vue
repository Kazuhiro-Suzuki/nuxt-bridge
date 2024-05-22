<template>
  <v-card elevation="2">
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-card-text>
      <v-form v-model="formValid">
        <v-row>
          <v-col cols="12" >
            <TextField
              label="お知らせのタイトル"
              :maxlength="subjectMaxLength"
              :rules="[$rules.required]"
              backgroundColor="white"
              @textFieldData="setSubject"
              :readonly="readonly"
            />
            <Editor
              class="editor-style"
              ref="editor"
              initialEditType="wysiwyg"
              :options="editorOptions"
              height="400px"
            />
          </v-col>
        </v-row>
        <v-row justify="center" align="center">
          <v-col xs="12" sm="12" md="5" lg="5">
            <VueCtkDateTimePicker
              v-model="newPost.active_since"
              label="お知らせの通知日時"
              :minute-interval="15"
              :format="'YYYY-MM-DD HH:mm'"
              :overlay="false"
              :rules="[$rules.required]"
              locale='ja'
              :color="baseColor"
            />
          </v-col>
          <v-col xs="12" sm="12" md="5" lg="5" v-if="is_disaster_info">
            <v-checkbox
              v-model="newPost.is_disaster_info"
              label="災害時のお知らせ"
            ></v-checkbox>
            <!-- バリデーション要追加 -->
          </v-col>
          <template v-if="segment_fileds">
            <v-col cols="12" sm="12" md="12" lg="12" xl="12">
              <p class="text-center">セグメント配信の項目を設定してください。</p>
            </v-col>
            <v-col  v-if="is_segment_birthday" xs="12" sm="12" md="12" lg="5" xl="5">
              <v-menu
                ref="birthDayMenu"
                v-model="birthDayMenu"
                :close-on-content-click="false"
                :return-value.sync="newPost.segment_birthday"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="newPost.segment_birthday"
                      label="誕生年月"
                      prepend-inner-icon="mdi-calendar"
                      readonly
                      outlined
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                </template>
                <v-date-picker
                  v-model="newPost.segment_birthday"
                  type="month"
                  :color="darkColor"
                  no-title
                  scrollable
                  locale="ja"
                  header-color="primary"
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
                    キャンセル
                  </v-btn>
                  <v-btn
                    text
                    :color="darkColor"
                    @click="$refs.birthDayMenu.save(newPost.segment_birthday)"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-menu>
            </v-col>
            <v-col  v-if="is_segment_birthday_year" xs="12" sm="12" md="12" lg="5" xl="5">
              <v-autocomplete
              v-model="newPost.segment_birthday_year"
              :items="yearOptions"
              label="誕生年"
              outlined
              multiple
              clearable
            ></v-autocomplete>
            </v-col>
            <!-- <v-col>
              <v-menu
                ref="menu"
                :close-on-content-click="false"
                v-model="menu"
                :nudge-right="40"
                lazy
                transition="scale-transition"
                prepend-inner-icon="mdi-calendar"
                offset-y
                full-width
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-combobox
                    v-model="newPost.is_segment_birthday_year"
                    multiple
                    chips
                    small-chips
                    label="誕生年"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-combobox>
                </template>
                <v-date-picker
                  ref="picker"
                  v-model="newPost.is_segment_birthday_year"
                  @input="save"
                  reactive
                  locale="ja"
                >
                </v-date-picker>
              </v-menu>
            </v-col> -->
            <v-col v-if="is_segment_birthday_month" cols="12" sm="12" md="12" lg="5" xl="5" >
              <v-autocomplete
                  v-model="newPost.segment_birthday_month"
                  :items="monthOptions"
                  outlined
                  clearable
                  multiple
                  label="誕生月"
                ></v-autocomplete>
            </v-col>
            <v-col v-if="ageOptions.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5" >
              <v-autocomplete
                  v-model="newPost.segment_age_range"
                  :items="ageOptions"
                  outlined
                  clearable
                  multiple
                  label="年齢"
                ></v-autocomplete>
            </v-col>
            <v-col v-if="addrressOptions.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5" >
              <v-autocomplete
                  v-model="newPost.segment_address_block"
                  :items="addrressOptions"
                  outlined
                  clearable
                  multiple
                  label="お住まいの地名"
                ></v-autocomplete>
            </v-col>
            <v-col v-if="userTypeChoices.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5">
                <v-autocomplete
                  v-model="newPost.segment_user_type"
                  :items="userTypeChoices"
                  outlined
                  multiple
                  label="障害児者との関係"
                ></v-autocomplete>
              </v-col>
              <v-col v-if="disabilityTypeChoices.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5">
                <v-autocomplete
                  v-model="newPost.segment_disability_type"
                  :items="disabilityTypeChoices"
                  outlined
                  multiple
                  label="本人（家族等）の障害種別"
                ></v-autocomplete>
              </v-col>
              <v-col v-if="notificationTags.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5">
                <v-autocomplete
                  v-model="newPost.segment_notification_tag"
                  :items="notificationTags"
                  outlined
                  multiple
                  label="配信に関連したサービス"
                ></v-autocomplete>
              </v-col>
              <v-col v-if="notificationCategories.length !== 0" cols="12" sm="12" md="12" lg="5" xl="5">
                <v-autocomplete
                  v-model="newPost.segment_notification_category"
                  :items="notificationCategories"
                  item-value="text"
                  outlined
                  multiple
                  label="お知らせのカテゴリ"
                ></v-autocomplete>
              </v-col>
          </template>
        </v-row>
      </v-form>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions>
      <v-row>
        <v-col cols="12">
          <div class="text-center">
            <OutlinedButton
              text="確認する"
              :color="darkColor"
              :disabled="!formValid"
              @clickEvent1="validateForm"
            />
          </div>
        </v-col>
      </v-row>
    </v-card-actions>

  <v-dialog
    v-model="dialog"
    width="1000"
  >
    <ConfirmCard
      v-if="dialog"
      :title="title"
      :data="newPost"
      buttonText="投稿する"
      confirmTitle="お知らせを投稿しますか？"
      confirmButtonText="投稿する"
      btnClass="white--text px-10"
      :readonly="readonly"
      :baseColor="baseColor"
      :darkColor="darkColor"
      :subjectMaxLength="subjectMaxLength"
      :bodyMaxLength="bodyMaxLength"
      @clickEvent3="postNewNotification()"
    >
      <template v-slot:confirmText>
        <div class="black--text pt-6">
          投稿するとお知らせ配信の通知がメールで送信されます。内容の編集は後からでも行えます。 このお知らせ内容と設定で投稿してよろしいですか？
        </div>
      </template>
      <template v-slot:firstAction>
        <NormalButton
          text="キャンセル"
          darkColor="white"
          btnClass="px-10"
          @clickAction="dialog = !dialog"
        />
      </template>
    </ConfirmCard>
  </v-dialog>

  </v-card>
</template>

<script>
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker'
import { Editor } from '@toast-ui/vue-editor'
import '@toast-ui/editor/dist/i18n/ja-jp';
import { notificationField } from '@/model/NotificationField'

export default {
  components: {
    VueCtkDateTimePicker,
    Editor
  },
  props: {
    citycode: {
      type: String,
      required: true,
    },
    baseColor: {
      type: String,
      required: true,
    },
    darkColor: {
      type: String,
      required: true,
    },
    subjectMaxLength: {
      type: String,
      required: true,
    },
    bodyMaxLength: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      title: "お知らせ新規投稿",
      formValid: false,
      newPost: {
        subject: '',
        body: '',
        city_code: '',
        active_since: '',
        is_disaster_info: false,
        segment_birthday:'',
        segment_birthday_year: [],
        segment_birthday_month: [],
        segment_address_block: [],
        segment_age_range: [],
        segment_user_type: [],
        segment_disability_type:[],
        segment_notification_tag: [],
        segment_notification_category: [],
      },
      birthDayMenu:false,
      disabilityTypeChoices: [],
      userTypeChoices: [],
      addrressOptions:[],
      ageOptions:[],
      yearOptions: [],
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
      notificationTags: [],
      notificationCategories: [],
      segment_fileds: false,
      is_segment_birthday: false,
      is_segment_birthday_year: false,
      is_segment_birthday_month: false,
      dialog: false,
      readonly: true,
      timeout: 5000,
      fileIds:[],
      editorOptions: {
        initialEditType: 'wysiwyg',
        placeholder: 'お知らせの内容',
        language: 'ja',
        hooks: {
          addImageBlobHook: this.addImageBlobHook,
        },
      },
      // menu: false,
    }
  },
  methods: {
    setSubject(data) {
      this.newPost.subject = data
    },
    setBody(data) {
      this.newPost.body = data
    },
    validateForm(){
      const extractedMarkdown = this.$refs.editor.invoke('getMarkdown')
      this.setBody(extractedMarkdown)
      if (extractedMarkdown.length === 0) {
          this.$notifier.showMessage({ content: 'お知らせ内容を入力してください', color: 'error' })
          return false
      }
      if (this.newPost.active_since == '' || this.newPost.active_since == null) {
          this.$notifier.showMessage({ content: 'お知らせの通知日時を入力してください', color: 'error' })
          return false
      }

      if(this.is_segment_birthday){
        if(this.newPost.segment_birthday != '' && this.newPost.segment_birthday_month.length !== 0){
          this.$notifier.showMessage({ content: '誕生年月と誕生月はどちらか１つを指定してください。', color: 'error' })
            return false
        }
      }

      this.openDialog()
    },
    openDialog(){
      this.dialog = !this.dialog
    },
    async addImageBlobHook(blob, addImageCallback) {
      this.$emit('openDialog', true)
      const description = document.getElementById('toastuiAltTextInput')?.value
      const formData = new FormData()
      formData.append('files', blob)
      formData.append('city_code', this.citycode)
      formData.append('visible_scope', 'public')

      const config = {
        headers: {
          'content-type': 'multipart/form-data'
        },
      }
      const response = await this.$api.uploadAssets(formData, config)
      let file_id;
      if(response.status == 201 && response.data.uploaded_files.length > 0) {
        file_id = response.data.uploaded_files[0].id
        this.fileIds.push(file_id)
        
        addImageCallback(
          '/api/v1/app/upload_file/public/?file_id=' + file_id,
          description || response.data.uploaded_files[0].file_name
        )
      }else {
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '画像をアップロードできませんでした。', color: 'error' })
        }
      }
      this.$emit('openDialog', false)
    },
    async postNewNotification() {
      console.log("Post:", this.newPost);
      this.newPost.city_code = this.citycode
      this.newPost.file_ids = this.fileIds

      const response = await this.$api.postNotification(this.newPost)
      // console.log(response)
      if (response.status == 201) {
        this.dialog = false
        this.$notifier.showMessage({ content: '投稿が完了しました。', color: 'info' })
        this.$nuxt.refresh()
      } else {
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '投稿できませんでした。', color: 'error' })
        }
        this.dialog = false
      }
    },
    populateYears() {
      const currentYear = new Date().getFullYear();
      const startYear = currentYear - 100; // You can adjust the range as needed

      for (let year = startYear; year <= currentYear; year++) {
        this.yearOptions.push(year.toString());
      }
    },
    // save (date) {
    //   this.$refs.menu.save(date);
    //   this.$refs.picker.activePicker = 'YEAR'
    //   this.menu = false;
    // }
  },
  mounted() {
    this.populateYears();
  },
  // watch: {
  //   menu (val) {
  //     val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
  //   }
  // },
  created(){
    let notificationInfo = notificationField.find(item => item.city_code ==  this.citycode);
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


<style scoped>
.editor-style >>> .toastui-editor-contents {
 font-family: 'Hiragino Kaku Gothic, sans-serif';
}
</style>