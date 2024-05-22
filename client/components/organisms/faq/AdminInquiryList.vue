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
        <v-btn depressed icon @click="reloadUserList">
          <v-icon>mdi-sync</v-icon>
        </v-btn>
      </v-app-bar>
      <v-card-text>
        <v-data-table
          class="elevation-1"
          hide-default-footer
          no-data-text="データがありません"
          :items="items"
          :headers="headers"
          :items-per-page="itemPerPage"
          :page.sync="page"
          :search="search"
          :item-class="itemRowBackground"
          @page-count="pageCount = $event"
          @click:row="getUserInquiryDetail"
        >
          <template v-slot:[`item.created_at`]="{ item }">
            {{ created_at(item) }}
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
    citycode: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      headers: [
        { text: 'メールアドレス', sortable: true, value: 'created_by__email', width: '35%' },
        { text: '登録日', sortable: true, align: 'center', value: 'created_at', width: '35%' },
        { text: '要対応', sortable: true, align: 'center', value: 'status_sum', width: '30%' },
      ],
      page: 1,
      pageCount: 0,
      itemPerPage: 15,
      search: '',
    }
  },
  methods: {
    async getUserInquiryDetail(value) {
        this.$router.push(`/admin/faq/detail/${value.user_id}?citycode=${this.citycode}`)
    },
    created_at(item){
      if (item.created_at){
       return this.$moment(item.created_at).format('YYYY-MM-DD HH:mm')
      }else{
        return ''
      }
    },
    itemRowBackground(item){
      if (item.status_sum == 0){
        return "admin-inquiry-list-bg-color"
      }
    },
    async reloadUserList(){
      this.$nuxt.refresh()
    }
  }
}
</script>

<style>
.admin-inquiry-list-bg-color{
  background-color: #E0E0E0
}
.admin-inquiry-list-bg-color:hover{
  background-color: #E0E0E0 !important
}
</style>

