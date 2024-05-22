<template>
  <v-card>
    <DenseToolBar
      :title="title"
      :baseColor="baseColor"
    />
    <v-card-text>
      <v-text-field
        v-model="userInfo.email"
        label="メールアドレス"
        disabled
        outlined
      ></v-text-field>
      <v-autocomplete
        v-model="userInfo.facilities"
        label="施設名"
        :disabled="disabled"
        outlined
        multiple
        return-object
        :items="facilityItems"
        item-text="name"
        item-value="id"
        append-icon=""
      ></v-autocomplete>
      <!-- <v-autocomplete
        :items="items"
        item-text="name"
        item-value="id"
        outlined
      ></v-autocomplete> -->
    </v-card-text>
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
      disabled: true,
      facilityItems: []
    }
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
    }
  },
  async created(){
    const facilityResponse = await this.$api.getAllPublicFacilities(`city_code=${this.citycode}`)
    // console.log(response)
    if (facilityResponse.status == 200) {
      this.facilityItems = facilityResponse.data
    } else{
      if (facilityResponse.data.detail) {
        errorMessage = facilityResponse.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
  }
}
</script>