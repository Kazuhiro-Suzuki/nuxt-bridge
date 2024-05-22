<template>
  <v-container>
    <v-overlay v-if="showLoading" style="z-index: 206">
          <h2>読み込み中</h2>
    </v-overlay>
    <v-row>
      <v-col>
        <ErrorAlert :message="errorMessage" />
      </v-col>
    </v-row>
    <v-row justify="center" v-if="['142077'].includes(citycode)">
      <v-col xs="12">
        <v-btn
          x-large
          elevation="1"
          outlined
          :color="regionData.dark_color"
          @click="dialog = !dialog"
        >
          ダウンロード
      </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <UserListTable
          title="ユーザー一覧"
          :items="items"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :citycode="citycode"
        />
      </v-col>
    </v-row>
    <v-dialog
        v-model="dialog"
        :width="dialogWidth"
      >
        <Confirmation
          :isNormalButton="true"
          btnClass="white--text px-10"
          title="ユーザー情報のダウンロード"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          buttonText="ダウンロード"
          @clickAction1="getUserListCsv"
        >
          <template v-slot:userInfo>
              <p class="pt-6">個人情報が含まれるため、取り扱いに注意の上、ダウンロードしてください。</p>
              <p>ダウンロード後、本アプリ管理者全員に、通知が送付されます。</p>
          </template>
          <template v-slot:firstAction>
            <NormalButton
              text="キャンセル"
              darkColor="white"
              btnClass="px-10"
              @clickAction="dialog = !dialog"
            />
          </template>
        </Confirmation>
      </v-dialog>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  middleware: ['authenticated'],
  head() {
    return {
      title: 'ユーザー管理',
    }
  },
  data() {
    return {
      showLoading: false,
      dialog: false,
      dialogWidth: 400,
      title: 'ユーザー管理',
      citycode: this.$route.query.citycode,
      items: [],
      errorMessage: '',
    }
  },
  computed: {
    ...mapState({
      regionData: state => state.region.regionData
    })
  },
  methods: {
    async getUserListCsv(){
      this.showLoading = !this.showLoading
      const response = await this.$api.getUserListCsv(`city_code=${this.citycode}`)
      if (response.status == 200) {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'user-list.csv'); 
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url);
        this.$notifier.showMessage({ content: 'ダウンロードが完了しました。', color: 'info' })
      } else{
        if (response.data.detail) {
          errorMessage = response.data.detail
        } else {
          errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
        }
      }
      this.dialog = !this.dialog
      this.showLoading = !this.showLoading
    }
  },
  async asyncData({ route, $api }) {
    let items = []
    let errorMessage = ''
    const response = await $api.getUserList(`city_code=${route.query.citycode}`)
    // console.log(response)
    if (response.status == 200) {
      items = response.data
    } else{
      if (response.data.detail) {
        errorMessage = response.data.detail
      } else {
        errorMessage = 'サーバーエラーです、時間置いてからお試しください。'
      }
    }
    return {
      items,
      errorMessage,
    }
  }
}
</script>