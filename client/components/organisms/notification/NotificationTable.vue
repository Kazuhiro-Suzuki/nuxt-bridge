<template>
  <div>
    <v-card elevation="2">
      <DenseToolBar
        :title="title"
        :baseColor="baseColor"
      />
      <v-card-text>
        <v-data-table
          class="elevation-1"
          hide-default-footer
          no-data-text="データがありません"
          :items="items"
          :headers="headers"
          :items-per-page="itemPerPage"
          :page.sync="page"
          @page-count="pageCount = $event"
        >
          <template v-slot:[`item.active_since`]="{ item }">
            {{ $moment(item.active_since).format('YYYY-MM-DD HH:mm') }}
          </template>
          <!-- <template v-slot:[`item.is_active`]="{ item }">
            <p v-if="item.is_active==true">有効</p>
            <p v-else>無効</p>
          </template> -->
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
    </v-card>

    <!-- 詳細確認ダイアログ -->
    <v-dialog
      v-model="detailDialog"
      :width="dialogWidth"
    >
      <ConfirmCard
        v-if="detailDialog"
        title="お知らせ詳細"
        :data="targetItem"
        :readonly="detailReadOnly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        :subjectMaxLength="subjectMaxLength"
        :bodyMaxLength="bodyMaxLength"
        @clickEvent3="detailDialog = !detailDialog"
        buttonText="閉じる"
      />
    </v-dialog>

    <!-- 編集ダイアログ -->
    <v-dialog
      v-model="editDialog"
      :width="dialogWidth"
    >
      <ConfirmCard
        v-if="editDialog"
        title="お知らせ編集"
        confirmTitle="お知らせを更新しますか？"
        confirmButtonText="更新する"
        btnClass="white--text px-10"
        :data="targetItem"
        :readonly="editReadOnly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        :subjectMaxLength="subjectMaxLength"
        :bodyMaxLength="bodyMaxLength"
        @clickEvent3="putNotification(targetItem)"
        @openDialog="$emit('openDialog', $event)"
        buttonText="編集する"
      >
        <template v-slot:confirmText>
          <p class="black--text pt-6">
            このお知らせ内容と設定で更新してよろしいですか？
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
      </ConfirmCard>
    </v-dialog>

    <!-- 削除確認ダイアログ -->
    <v-dialog
      v-model="deleteDialog"
      :width="dialogWidth"
    >
      <ConfirmCard
        v-if="deleteDialog"
        title="お知らせ削除"
        confirmTitle="お知らせを削除しますか？"
        confirmButtonText="削除する"
        btnClass="white--text px-10"
        :data="targetItem"
        :readonly="deleteReadOnly"
        :baseColor="baseColor"
        :darkColor="darkColor"
        :subjectMaxLength="subjectMaxLength"
        :bodyMaxLength="bodyMaxLength"
        @clickEvent3="deleteNotification(targetItem)"
        buttonText="削除する"
      >
        <template v-slot:firstAction>
          <NormalButton
            text="キャンセル"
            darkColor="white"
            btnClass="px-10"
            @clickAction="deleteDialog = !deleteDialog"
          />
        </template>
      </ConfirmCard>
    </v-dialog>

  </div>
</template>

<script>
export default {
  props: {
    citycode: {
      type: String,
      required: true,
    },
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
      required: true,
    },
    bodyMaxLength: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      headers: [
        { text: 'タイトル', sortable: false, align: 'start', value: 'subject', width: '60%' },
        { text: '通知日時', sortable: true, align: 'start', value: 'active_since', width: '20%' },
        // { text: 'ステータス', sortable: false, align: 'center', value: 'is_active' },
        { text: '詳細 / 編集 / 削除', sortable: false, align: 'start', value: 'actions', width: '20%' },
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
    }
  },
  methods: {
    async detailItem(item) {
      const response = await this.$api.getNotificationDetail(item.id)
      if (response.status == 200) {
        this.targetItem = Object.assign({}, response.data[0])
        this.detailDialog = true
      }
      else {
        if (response.data.detail) {
          this.$notifier.showMessage({ content: response.data.detail, color: 'error' })
        } else {
          this.$notifier.showMessage({ content: '表示できませんでした、時間を置いてやり直してください。' , color: 'error' })
        }
      }
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
    async putNotification(targetItem) {
      const response = await this.$api.putNotification(targetItem)
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
    async deleteNotification(targetItem) {
      const response = await this.$api.deleteNotification(targetItem.id)
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
    }
  }
}
</script>

