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
    }
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
  },
}
</script>