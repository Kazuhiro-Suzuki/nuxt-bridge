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
              v-if="($auth.loggedIn && $auth.user.type === 'business')"
              label="表示名"
              :maxlength="displayNameMaxLength"
              :rules="[$rules.required]"
              @textFieldData="setDisplayName"
            />
            <SelectBox
                label="お問い合わせ種別"
                :choices="choices"
                :inputMode="true"
                :rules="[$rules.required]"
                @selectBoxData="setCategory"
            />
            <TextArea
              label="お問い合わせの内容"
              :maxlength="bodyMaxLength"
              :rules="[$rules.required]"
              backgroundColor="white"
              @textAreaData="setBody"
              :readonly="readonly"
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-row>
        <v-col cols="12">
          <div class="text-center">
            <OutlinedButton
              text="送信"
              :color="darkColor"
              :disabled="!formValid"
              @clickEvent1="postNewInquiry()"
            />
          </div>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
import { inquiryChoices } from '../../../model/inquiryChoices'

export default {
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
    bodyMaxLength: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      title: "お問い合わせ新規投稿",
      formValid: false,
      choices: [
        // { text: '本アプリの活用方法', id: 'app' },
        // { text: 'お知らせ内容', id: 'notification' },
        // { text: '会員登録', id: 'registration' },
        // { text: 'ミライロID', id: 'mirairo' },
        // { text: '短期入所施設予約', id: 'reservation' },
        // { text: 'ご意見、その他', id: 'other' },
      ],
      newPost: {
        display_name: '',
        category: '',
        contents: '',
      },
      readonly: true,
      timeout: 5000,
      displayNameMaxLength: '256',
    }
  },
  methods: {
    setBody(data) {
      console.log(this.darkColor);
      this.newPost.contents = data
    },
    setCategory(data) {
      this.newPost.category = data[0]
    },
    setDisplayName(data){
      this.newPost.display_name = data
    },
    async postNewInquiry() {
      let response 
      if (this.$auth.loggedIn && ['general','facility'].includes(this.$auth.user.type)) {
        response = await this.$api.postNewInquiry(this.newPost, `city_code=${this.citycode}`)
      }else{
        response = await this.$api.postNewReply(this.newPost, `city_code=${this.citycode}`, this.$route.params.userId)
      }
      
      if (response.status == 201) {
        this.$notifier.showMessage({ content: '投稿が完了しました。', color: 'info' })
        this.$nuxt.refresh()
      } else {
        console.log(response);
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '投稿できませんでした。', color: 'error' })
        }
        this.newPost.contents, this.newPost.category, this.newPost.category = '', '', ''
      }
    }
  },
  created() {
    let inquiryInfo = inquiryChoices.find(item => item.city_code ==  this.citycode);
    this.choices = inquiryInfo.choices
  },
}
</script>