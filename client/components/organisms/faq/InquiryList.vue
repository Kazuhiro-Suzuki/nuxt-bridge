<template>
  <v-row>
    <v-col
      cols="12"
      v-for="item in inquiryItems"
      :key=item.id
    >
      <v-card :color="color(item)">
        <v-row>
          <v-col sm="9" md="9" lg="9" xl="9">
             <v-card-title class="text-h6">
              {{ displayName(item) }}
            </v-card-title>
          </v-col>
          <v-col sm="3" md="3" lg="3" xl="3" class="text-right">
             <v-card-subtitle>
              {{ $moment(item.created_at).format('YYYY-MM-DD HH:mm') }}
            </v-card-subtitle>
          </v-col>
        </v-row>
        <v-card-text>
          <div
            v-if="($auth.loggedIn && $auth.user.type === 'business' && item.message_type === 'inquiry')" 
            class="d-sm-flex d-md-flex d-lg-flex align-center justify-sm-space-between justify-md-space-between justify-lg-space-between">
            <div>
              <div class="font-weight-bold pb-1">お問い合わせステータス</div>
              <div class="px-1 pb-1">{{status(item)}}</div>
            </div>
            <v-card-actions class="pr-0">
              <NormalButton
                  text="対応中にする"
                  :btnClass="`${baseColor} lighten-4`"
                  :color="baseColor"
                  :disabled="!isPending(item)"
                  @clickAction="updateInquiryStatus('inspecting', item.id)"
                />
              <NormalButton
                text="対応終了にする"
                :btnClass="`${baseColor} lighten-4`"
                :color="baseColor"
                :disabled="!isNotCompleted(item)"
                @clickAction="updateInquiryStatus('completed', item.id)"
              />
            </v-card-actions>
          </div>
          <div class="font-weight-bold pb-1">お問い合わせ種別</div>
          <div class="px-1 pb-1">{{ category(item) }}</div>
          <div class="font-weight-bold pb-1">お問い合わせ内容</div>
          <div class="px-1">{{ item.contents }}</div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    inquiryItems: {
      type: Array,
      required: true
    },
    baseColor: {
      type: String,
      required: true
    },
    citycode: {
      type: String,
      required: true
    }
  },
  computed: {
    displayName: function(){
      return function(item){
        if (this.$auth.loggedIn && ['general','facility'].includes(this.$auth.user.type) && item.message_type === 'inquiry') {
          return 'あなた'
        }else{
          return item.display_name
        } 
      }
    },
    category: function(){
      const choices = { 
        app: '本アプリの活用方法',
        notification: 'お知らせ内容',
        registration: '会員登録',
        mirairo: 'ミライロID',
        reservation: '短期入所施設予約',
        reserve_consult: 'オンライン相談予約',
        support_file: 'るぴなすノート',
        other: 'ご意見、その他'
      }
      return function(item){
        return choices[item.category]
      }
    },
    color: function(){
      return function(item){
        if (item.message_type === 'reply') {
          return 'grey lighten-2'
        }else{
          return ''
        } 
      }
    },
    status(){
      const status = {
        pending: '未対応',
        inspecting: '対応中',
        completed: '対応済み'
      }
      return function(item){
        return status[item.status]
      }
    },
    isPending(item){
      return function(item){
        if(item.status === "pending"){
          return true
        }else{
          return false
        }
      }
    },
    isNotCompleted(item){
      return function(item){
        if(item.status !== "completed"){
          return true
        }else{
          return false
        }
      }
    }
  },
  methods: {
    async updateInquiryStatus(status, id) {
      const payload = {
        'status': status,
        'id': id
      }
      const response = await this.$api.updateInquiryStatus(payload, `city_code=${this.citycode}`, this.$route.params.userId)
      if (response.status == 200) {
        this.$notifier.showMessage({ content: 'ステータスの更新が完了しました。', color: 'info' })
        this.$nuxt.refresh()
      } else {
        console.log(response);
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: 'ステータスを更新できませんでした。', color: 'error' })
        }
      }
    }
  },
}
</script>
