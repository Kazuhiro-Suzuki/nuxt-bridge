<template>
  <v-card elevation="2">
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-card-text>
      <v-form v-model="formValid">
        <v-row justify="center">
          <v-col cols="6">
            <!-- <TextField
              label="郵便番号"
              maxlength="7"
              :rules="[$rules.required, $rules.halfNum]"
              @textFieldData="setPostalCode"
              :readonly="readonly"
            />
          </v-col>
          <v-col cols="6">
            <TextField
              label="電話番号"
              maxlength="15"
              :rules="[$rules.required, $rules.halfNum]"
              @textFieldData="setPhoneNumber"
              :readonly="readonly"
            /> -->
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12">
            <TextField
              label="名称"
              maxlength="100"
              :rules="[$rules.required]"
              @textFieldData="setName"
              :readonly="readonly"
            />
            <!-- <TextField
              label="住所"
              maxlength="100"
              :rules="[$rules.required]"
              @textFieldData="setAddress"
              :readonly="readonly"
            /> -->
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

    <v-dialog
      v-model="dialog"
      width="600"
    >
      <ConfirmFacility
        :title="title"
        :data="newPost"
        buttonText="登録する"
        :readonly="readonly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        @clickEvent3="postNewFacility"
      />
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
  },
  data() {
    return {
      title: "施設新規追加",
      formValid: false,
      newPost: {
        postal_code: '',
        phone_number: '',
        name: '',
        address: '',
      },
      dialog: false,
      readonly: true,
      timeout: 5000,
    }
  },
  methods: {
    setName(data) {
      this.newPost.name = data
    },
    setAddress(data) {
      this.newPost.address = data
    },
    setPostalCode(data) {
      this.newPost.postal_code = data
    },
    setPhoneNumber(data) {
      this.newPost.phone_number = data
    },
    async postNewFacility() {
      this.$emit('showLoading', true)
      this.newPost.city_code = this.citycode
      const response = await this.$api.postFacility(this.newPost)
      // console.log(response)
      if (response.status == 201) {
        this.dialog = false
        this.$notifier.showMessage({ content: '登録が完了しました。', color: 'info' })
        this.$nuxt.refresh()
      } else {
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '登録できませんでした。', color: 'error' })
        }
        this.dialog = false
      }
      this.$emit('showLoading', false)
    }
  },
}
</script>