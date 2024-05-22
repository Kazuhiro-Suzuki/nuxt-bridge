<template>
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
        :headers="headers"
        :items="filter(items)"
        :items-per-page="itemPerPage"
        :page.sync="page"
        :search="search"
        :custom-filter="customSearch"
        @page-count="pageCount = $event"
      >
        <template align="center" v-slot:[`item.facilities`]="{ item }">
          <div class="py-2">
            <span 
              v-for="(facility, i) in item.facilities" 
              :key=i
              style="display: block;">{{ facility.name }}</span>
          </div>
        </template>
        <template v-slot:[`item.date_joined`]="{ item }">
          {{ $moment(item.date_joined).format('YYYY-MM-DD HH:mm') }}
        </template>
        <template align="center" v-slot:[`item.is_active`]="{ item }">
          <p v-if="item.is_active">有効</p>
          <p v-else>無効</p>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon @click="showDialog(item)" class="mr-2">
            mdi-sync
          </v-icon>
        </template>
        <template v-slot:[`item.edit`]="{ item }">
            <v-icon @click="editItem(item)" class="mr-2">
              mdi-pencil
            </v-icon>
            <v-icon @click="deleteItem(item)" class="mr-2">
              mdi-delete
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
        @clickEvent2="putUserInfo(targetItem)"
      />
    </v-dialog>
    
    <!-- 編集ダイアログ -->
    <v-dialog
      v-model="editDialog"
      width="600"
    >
      <ConfirmFacilityUser
        v-if="editDialog"
        title="施設ユーザー編集"
        confirmTitle="施設ユーザーを更新しますか？"
        confirmButtonText="更新する"
        btnClass="white--text px-10"
        :data="targetItem"
        :readonly="editReadOnly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        :items="facilityItems"
        @clickEvent3="putFacilityUser(targetItem)"
        buttonText="編集する"
      >
        <template v-slot:confirmText>
          <p class="black--text pt-6">
            この内容と設定で更新してよろしいですか？
          </p>
        </template>
        <template v-slot:firstAction>
          <NormalButton
            text="キャンセル"
            darkColor="white"
            btnClass="px-10"
            @clickAction="editDialog = !editDialog"
          />
        </template>
      </ConfirmFacilityUser>
    </v-dialog>

    <!-- 削除確認ダイアログ -->
    <v-dialog
      v-model="deleteDialog"
      width="600"
    >
      <ConfirmFacilityUser
        v-if="deleteDialog"
        title="施設ユーザー削除"
        confirmTitle="施設ユーザーを削除しますか？"
        confirmButtonText="削除する"
        buttonText="削除する"
        btnClass="white--text px-10"
        :data="targetItem"
        :items="facilityItems"
        :readonly="deleteReadOnly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        @clickEvent3="deleteFacilityUser(targetItem)"
      >
        <template v-slot:firstAction>
          <NormalButton
            text="キャンセル"
            darkColor="white"
            btnClass="px-10"
            @clickAction="deleteDialog = !deleteDialog"
          />
        </template>
      </ConfirmFacilityUser>
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
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
    facilityItems: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      headers: [
        { text: '施設名', sortable: true, value: 'facilities', width: '35%' },
        { text: 'メールアドレス', sortable: true, value: 'email', width: '35%' },
        { text: 'ログイン', sortable: true, align: 'center', value: 'is_active', width: '10%' },
        { text: '操作', sortable: false, align: 'center', value: 'actions', width: '10%' },
        { text: '編集 / 削除', sortable: false, align: 'center', value: 'edit', width: '10%' },
      ],
      page: 1,
      pageCount: 0,
      itemPerPage: 15,
      dialogWidth: 400,
      dialog: false,
      deleteDialog: false,
      editDialog: false,
      editReadOnly: false,
      deleteReadOnly: true,
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
      targetItem.is_active = !targetItem.is_active
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
    },
    editItem(item) {
      this.targetIndex = this.items.indexOf(item)
      this.targetItem = Object.assign({}, item)
      this.editDialog = true
    },
    deleteItem(item) {
      this.targetIndex = this.items.indexOf(item)
      this.targetItem = Object.assign({}, item)
      this.deleteDialog = true
    },
    async putFacilityUser(targetItem) {
      let payload = {
        'uid': targetItem.uid,
        'email': targetItem.email,
        'phone_number': null,
        'fax_number': null,
        'is_subscribe': targetItem.is_subscribe,
        'facilities': targetItem.facilities,
        'get_disaster_notification': true,
        'get_notification': true
      }
      let response = await this.$api.putUserInfo(payload)
      // console.log(response)
      if (response.status == 200) {
        this.editDialog = false
        this.$notifier.showMessage({ content: '編集が完了しました。', color: 'info' })
        this.$nuxt.refresh()
      } else {
        this.editDialog = false
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '編集できませんでした、時間を置いてやり直してください。' , color: 'error' })
        }
      }
      this.targetIndex = -1
      this.targetItem = {}
    },
    async deleteFacilityUser(targetItem) {
      let response = await this.$api.deleteUserInfo(targetItem)
      // console.log(response)
      if (response.data) {
        this.deleteDialog = false
        this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
      } else {
        this.deleteDialog = false
        this.$notifier.showMessage({ content: '削除が完了しました。', color: 'info' })
        this.$nuxt.refresh()
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
    },
    customSearch (value, search, item) {
      if (Array.isArray(value)) {
          return value.some(item=>Object.values(item).some(v=>v&&v.toString().toLowerCase().includes(search)))
      }
      return Object.values(item).some(v=>v&&v.toString().toLowerCase().includes(search))
    }
  },
}
</script>