<template>
  <v-card elevation="2">
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-card-text>
      <v-form v-model="formValid">
        <v-row justify="center">
          <v-col cols="12">
            <TextField
              label="メールアドレス"
              maxlength="100"
              icon="mdi-mail"
              :rules="[$rules.required]"
              @textFieldData="setEmail"
            />
            <v-autocomplete
                v-model="newPost.facilities"
                :items="items"
                item-text="name"
                item-value="id"
                :search-input.sync="search"
                return-object
                outlined
                clearable
                multiple
                :rules="[$rules.required]"
                label="施設名"
                @change="search = ''"
            ></v-autocomplete>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions>
      <v-row justify="center">
        <v-col cols="8">
          <div class="text-center">
            <OutlinedButton
              text="確認する"
              :color="darkColor"
              :disabled="!formValid"
              @clickEvent1="dialog = !dialog"
            />
          </div>
        </v-col>
      </v-row>
    </v-card-actions>

  <!-- これから登録する内容の確認ダイアログ -->
    <v-dialog
      v-model="dialog"
      width="600"
    >
      <ConfirmFacilityUser
        :title="title"
        :data="newPost"
        :items="items"
        buttonText="登録する"
        confirmTitle="施設ユーザーを登録しますか？"
        confirmButtonText="登録する"
        btnClass="white--text px-10"
        :readonly="readonly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        @clickEvent3="postNewFacilityUser"
      >
        <template v-slot:firstAction>
          <NormalButton
            text="キャンセル"
            darkColor="white"
            btnClass="px-10"
            @clickAction="dialog = !dialog"
          />
        </template>
      </ConfirmFacilityUser>
    </v-dialog>

    <!-- 登録が完了したユーザー情報の確認ダイアログ -->
    <v-dialog
      v-model="userInfoDialog"
      width="600"
    >
      <Confirmation
        title="確認"
        :baseColor="baseColor"
        buttonText="閉じる"
        @clickEvent2="userInfoDialog = !userInfoDialog"
      >
        <template v-slot:userInfo>
          <p class="text-h6 text-center py-6" style="color:red">
            パスワードを必ずメモしてください。
          </p>
          <v-text-field
              v-if="userInfo.email"
              v-model="userInfo.email"
              label="メールアドレス"
              outlined
              :readonly="readonly"
            ></v-text-field>
            <v-text-field
              v-if="userInfo.name"
              v-model="userInfo.name"
              label="施設名"
              outlined
              multiple
              :readonly="readonly"
            ></v-text-field>
            <v-text-field
              v-if="userInfo.password"
              v-model="userInfo.password"
              label="パスワード"
              outlined
              maxlength="100"
              :readonly="readonly"
            ></v-text-field>
        </template>
      </Confirmation>
    </v-dialog>

  </v-card>
</template>

<script>
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
    items: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      title: "施設ユーザー新規追加",
      formValid: false,
      newPost: {
        email: '',
        type: 'facility',
        facilities: []
      },
      search: null,
      dialog: false,
      userInfoDialog: false,
      userInfo: {},
      readonly: true,
      timeout: 5000,
    }
  },
  methods: {
    setEmail(value) {
      this.newPost.email = value
    },
    async postNewFacilityUser() {
      this.newPost.city_code = this.citycode
      console.log(this.newPost);
      const response = await this.$api.postSignUpFacilityUserInfo(this.newPost)
      // console.log(response)
      if (response.status == 201) {
        this.dialog = false
        this.userInfo = response.data
        this.userInfoDialog = true
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
    }
  },
}
</script>