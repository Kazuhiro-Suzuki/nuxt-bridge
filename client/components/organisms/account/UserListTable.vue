<template>
  <div>
    <v-card elevation="2">
      <v-app-bar
        :class="`${baseColor} lighten-4 font-weight`"
        :color="baseColor"
        elevation="0"
      >
        <v-toolbar-title>
          {{ title }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-app-bar>
      <v-card-text>
        <v-data-table
          class="elevation-1"
          hide-default-footer
          no-data-text="データがありません"
          :items="filter(items)"
          :headers="headers"
          :items-per-page="itemPerPage"
          :page.sync="page"
          :search="search"
          @page-count="pageCount = $event"
        >
          <template v-slot:[`item.date_joined`]="{ item }">
            {{ $moment(item.date_joined).format('YYYY-MM-DD HH:mm') }}
          </template>
          <template v-slot:[`item.is_subscribe`]="{ item }">
            <p v-if="item.is_subscribe">有効</p>
            <p v-else>無効</p>
          </template>
          <template v-slot:[`item.is_active`]="{ item }">
            <p v-if="item.is_active">有効</p>
            <p v-else>無効</p>
          </template>
          <template v-if="citycode == '142077'" v-slot:[`item.is_dangerous`]="{ item }">
            <v-btn
              @click="putUserInfo(item, 'personStatus')"
              icon
            >
              <v-icon :color="!item.is_dangerous ? 'grey':'orange'">
                mdi-account-alert
              </v-icon>
            </v-btn>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon @click="showDialog(item)" class="mr-2">
              mdi-sync
            </v-icon>
          </template>
        </v-data-table>
      </v-card-text>

      <v-card-actions class="justify-center">
        <v-pagination
          v-model="page"
          :length="pageCount"
          :color="`${baseColor}`"
        ></v-pagination>
      </v-card-actions>
    </v-card>

    <!-- ステータス切替確認ダイアログ -->
    <v-dialog
      v-model="dialog"
      :width="dialogWidth"
    >
      <Confirmation
        title="確認"
        :baseColor="baseColor"
        :darkColor="darkColor"
        buttonText="ログインを切り替える"
        @clickEvent2="putUserInfo(targetItem, 'loginStatus')"
      >
        <template v-slot:firstAction>
          <TextButton
            text="メール配信を切り替える"
            :color="darkColor"
            @clickEvent1="putUserInfo(targetItem, 'emailStatus')"
          />
        </template>
      </Confirmation>
    </v-dialog>

  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    items: {
      type: Array,
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
      required: false,
    },
    bodyMaxLength: {
      type: String,
      required: false,
    },
    //港区改修後に削除予定
    citycode: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      headers: [],
      page: 1,
      pageCount: 0,
      itemPerPage: 15,
      dialogWidth: 400,
      dialog: false,
      targetIndex: -1,
      targetItem: {},
      search: '',
    }
  },
  methods: {
    showDialog(item) {
      this.dialog = true
      this.targetIndex = this.items.indexOf(item)
      this.targetItem = Object.assign({}, item)
      // console.log(this.targetIndex, this.targetItem)
    },
    async putUserInfo(targetItem, status) {
      if(status === 'loginStatus'){
        targetItem.is_active = !targetItem.is_active
      }
      if(status === 'emailStatus'){
        targetItem.is_subscribe = !targetItem.is_subscribe
      }
      if(status === 'personStatus'){
        targetItem.is_dangerous = !targetItem.is_dangerous
      }
      console.log(targetItem);
      const response = await this.$api.changeUserStatus(targetItem)
      // console.log(response)
      if (response.status == 200) {
        this.dialog = false
        this.$notifier.showMessage({ content: '切替が完了しました。', color: 'info' })
        this.$nuxt.refresh()
      } else {
        this.dialog = false
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '切替できませんでした、時間を置いてやり直してください。' , color: 'error' })
        }
      }
      this.targetIndex = -1
      this.targetItem = {}
    },
    filter(items){
      items = items.filter((item) => {
        if(item.email.includes("@deleted.com") && !item.is_active){
          return false
        }
        return true
      })
      return items;
    }
  },
  //港区改修後に削除予定
  created(){
    if(this.citycode == "142077"){
      this.headers.push(
          { text: 'メールアドレス', sortable: true, value: 'email', width: '20%' },
          { text: '電話番号', sortable: true, align: 'start', value: 'phone_number', width: '15%' },
          { text: 'FAX番号', sortable: true, align: 'start', value: 'fax_number', width: '10%' },
          { text: 'メール配信', sortable: false, align: 'center', value: 'is_subscribe', width: '10%' },
          { text: 'ログイン', sortable: false, align: 'center', value: 'is_active', width: '10%' },
          { text: '登録日', sortable: true, align: 'center', value: 'date_joined', width: '15%' },
          { text: '要配慮者', sortable: false, align: 'center', value: 'is_dangerous', width: '10%' },
          { text: '操作', sortable: false, align: 'center', value: 'actions', width: '10%' },
      )
    }
    if(['131032', '131237', '212172', '092134'].includes(this.citycode)){
      this.headers.push(
          { text: 'メールアドレス', sortable: true, value: 'email', width: '20%' },
          { text: '電話番号', sortable: true, align: 'start', value: 'phone_number', width: '15%' },
          { text: 'FAX番号', sortable: true, align: 'start', value: 'fax_number', width: '10%' },
          { text: 'メール配信', sortable: false, align: 'center', value: 'is_subscribe', width: '10%' },
          { text: 'ログイン', sortable: false, align: 'center', value: 'is_active', width: '10%' },
          { text: '登録日', sortable: true, align: 'center', value: 'date_joined', width: '15%' },
          { text: '操作', sortable: false, align: 'center', value: 'actions', width: '10%' },
      )
    }
  }
}
</script>

