<template>
  <v-container>
    <v-row>
      <v-col>
        <ErrorAlert :message="errorMessage" />
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col xs="12" sm="12" md="8" lg="8" xl="8">
        <NewNoticePost
          :citycode="citycode"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :subjectMaxLength="subjectMaxLength"
          :bodyMaxLength="bodyMaxLength"
          @openDialog="openDialog"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <NotificationTable
          :title="title"
          :items="items"
          :citycode="citycode"
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :subjectMaxLength="subjectMaxLength"
          :bodyMaxLength="bodyMaxLength"
          @openDialog="openDialog"
        />
      </v-col>
    </v-row>
    <v-dialog
        v-model="isUploading"
        persistent
        width="300"
        overlay-opacity="0.2"
      >
        <v-card color="rhb-accent">
          <div class="pa-4">
            <v-progress-circular
              indeterminate
              color="white"
            ></v-progress-circular>
            <span class="uploading-dialog-text">画像読み込み中...</span>
          </div>
        </v-card>
      </v-dialog>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  middleware: ['authenticated'],
  head() {
    return {
      title: 'お知らせ管理'
    }
  },
  data() {
    return {
      title: 'お知らせ管理',
      requestDateTime: '',
      items: [],
      citycode: this.$route.query.citycode,
      errorMessage: '',
      subjectMaxLength: '250',
      bodyMaxLength: '2000',
      errorMessage: '',
      isUploading: false,
      fileIds: []
    }
  },
  computed: {
    ...mapState({
      regionData: state => state.region.regionData
    })
  },
  async asyncData({ route, $api }) {
    let items = []
    let errorMessage = ''
    const response = await $api.getNotification(`city_code=${route.query.citycode}`)
    // console.log(response)
    if (response.status == 200) {
      items = response.data
    } else {
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
  },
  methods: {
    openDialog(bool){
      this.isUploading = bool
    },
  }
}
</script>
