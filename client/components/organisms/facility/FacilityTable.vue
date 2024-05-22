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
        :items="items"
        :items-per-page="itemPerPage"
        :page.sync="page"
        :search="search"
        @page-count="pageCount = $event"
      >
        <template v-slot:[`item.created_at`]="{ item }">
          {{ $moment(item.created_at).format('YYYY-MM-DD HH:mm') }}
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon @click="detailItem(item)" class="mr-2">
            mdi-comment-text
          </v-icon>
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

    <!-- 詳細ダイアログ -->
    <v-dialog
      v-model="detailDialog"
      width="600"
    >
      <ConfirmFacility
        title="施設詳細"
        :data="targetItem"
        buttonText="閉じる"
        :readonly="detailReadOnly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        @clickEvent3="detailDialog = !detailDialog"
      />
    </v-dialog>

    <!-- 編集ダイアログ -->
    <v-dialog
      v-model="editDialog"
      width="600"
    >
      <ConfirmFacility
        title="施設編集"
        :data="targetItem"
        buttonText="編集する"
        :readonly="editReadOnly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        @clickEvent3="putFacility(targetItem)"
      />
    </v-dialog>

    <!-- 削除ダイアログ -->
    <v-dialog
      v-model="deleteDialog"
      width="600"
    >
      <ConfirmFacility
        title="施設削除"
        :data="targetItem"
        buttonText="削除する"
        :readonly="deleteReadOnly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        @clickEvent3="deleteFacility(targetItem)"
      />
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
      required: false,
    },
    items: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      headers: [
        { text: '施設名', sortable: true, value: 'name', width: '40%' },
        // { text: '電話番号', sortable: false, value: 'phone_number', width: '20%' },
        { text: '登録日時', sortable: false, value: 'created_at', width: '20%' },
        { text: '操作', sortable: false, value: 'actions', align: 'center', width: '20%' },
      ],
      page: 1,
      pageCount: 0,
      itemPerPage: 10,
      dialogWidth: 1000,
      detailDialog: false,
      editDialog: false,
      deleteDialog: false,
      detailReadOnly: true,
      editReadOnly: false,
      deleteReadOnly: true,
      targetIndex: -1,
      targetItem: {},
      search: '',
    }
  },
  methods: {
    detailItem(item) {
      this.targetItem = Object.assign({}, item)
      this.detailDialog = true
    },
    editItem(item) {
      this.targetIndex = this.items.indexOf(item)
      this.targetItem = Object.assign({}, item)
      // console.log(this.targetIndex, this.targetItem)
      this.editDialog = true
    },
    deleteItem(item) {
      this.targetIndex = this.items.indexOf(item)
      this.targetItem = Object.assign({}, item)
      // console.log(this.targetIndex, this.targetItem)
      this.deleteDialog = true
    },
    async putFacility(targetItem) {
      this.$emit('showLoading', true)
      const response = await this.$api.putFacility(targetItem)
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
      this.$emit('showLoading', false)
    },
    async deleteFacility(targetItem) {
      this.$emit('showLoading', true)
      const response = await this.$api.deleteFacility(targetItem.id)
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
      this.$emit('showLoading', false)
    }
  },
}
</script>