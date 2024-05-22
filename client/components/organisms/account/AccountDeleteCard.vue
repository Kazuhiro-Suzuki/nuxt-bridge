<template>
  <div>
    
    <v-card>
      <DenseToolBar
        :title="title"
        :baseColor="baseColor"
      />
      <v-card-text>
        <div class="text-center">退会をご希望の方は「退会する」ボタンをクリックしてください。</div>
        <v-card-actions class="justify-center">
          <NormalButton
            text="退会する"
            :class="`${baseColor} lighten-3`"
            :color="baseColor"
            @clickAction="showDialog()"
          />
        </v-card-actions>
      </v-card-text>
    </v-card>
    <!--  退会確認ダイアログ -->
    <v-dialog
      v-model="dialog"
      :width="dialogWidth"
    >
      <Confirmation
        title="確認"
        :baseColor="baseColor"
        :darkColor="darkColor"
        buttonText="退会する"
        @clickEvent2="deleteUserInfo()"
      >
      </Confirmation>
    </v-dialog>
  </div>
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
    userInfo: {
      type: Object,
      required: true,
    },
    citycode: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      dialog: false,
      dialogWidth: 400,
    }
  },
  methods: {
    showDialog() {
      this.dialog = true
    },
    async deleteUserInfo() {
      let response = await this.$api.deleteUserInfo(this.userInfo)
      if (response.status == 200) {
        this.logout()
      } else {
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '情報を更新できませんでした。', color: 'error' })
        }

      }
    },
    logout() {
      this.$auth.logout()
        .then(() => {
          this.$router.push(`/?citycode=${this.citycode}`)
          this.$notifier.showMessage({ content: '退会が完了しました。', color: 'info' })
        })
    },
  },
}
</script>