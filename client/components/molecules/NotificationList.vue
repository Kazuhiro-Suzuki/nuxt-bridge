<template>
  <v-card outlined elevation="1">
    <DenseToolBar
      :baseColor="baseColor"
      :title="title"
    />
    <v-card-text v-if="isNoArray && notificationCategories.length > 0">
      <v-tabs
        v-model="tab"
        :color="baseColor"
      >
        <v-tab
          v-for="(categoryItem, i) in notificationCategories"
          :key="i"
        >
          {{ categoryItem.text }}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item
          v-for="(categoryItem, i) in notificationCategories"
          :key="i"
        >
          <v-expansion-panels
            v-model="panel"
            accordion
            multiple
          >
            <v-expansion-panel
              v-for="(item, i) in filterCategory(categoryItem)"
              :key="i"
            >
              <v-expansion-panel-header>
                {{ item.subject }}
                <br />
                <br />
                {{ $moment(item.active_since).format('YYYY-MM-DD HH:mm') }}
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <Viewer
                  :initialValue="item.body"
                />
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-tab-item>
      </v-tabs-items>
     </v-card-text>
    <v-card-text v-else-if="isNoArray && notificationCategories.length == 0">
      <v-expansion-panels
        v-model="panel"
        accordion
        multiple
      >
        <v-expansion-panel
          v-for="(item, i) in filteredItems"
          :key="i"
        >
          <v-expansion-panel-header>
            {{ item.subject }}
            <br />
            <br />
            {{ $moment(item.active_since).format('YYYY-MM-DD HH:mm') }}
          </v-expansion-panel-header>
          <v-expansion-panel-content>
             <Viewer
              :initialValue="item.body"
            />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
    <v-card-text v-else>
      <div class="text--primary">該当するお知らせはありません。</div>
    </v-card-text>

  </v-card>
</template>

<script>
import { Viewer } from '@toast-ui/vue-editor'
import { notificationField } from '@/model/NotificationField'

export default {
  components: {
    Viewer
  },
  props: {
    items: {
      type: Array,
      required: true,
    },
    searchWord:{
      type: String,
      required: false,
    },
    citycode: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    baseColor: {
      type: String,
      required: true,
    }
  },
  data () {
    return {
      panel: [],
      tab: '',
      notificationCategories: []
    }
  },
  computed: {
    path() {
      return `/home?citycode=${this.citycode}`
    },
    isNoArray(){
      return Array.isArray(this.filteredItems) && this.filteredItems.length
    },
    filteredItems(){
      const items = this.items.filter((item) => {
        if(item.body.includes(this.searchWord) || item.subject.includes(this.searchWord)){
          return true
        }
      })
      return items;
    },
  },
  methods: {
    filterCategory(categoryItem){
      let newItems = this.filteredItems.filter((filteredItem) => {
        if(categoryItem.value == 0){
          return true
        }
        if(filteredItem.segment_notification_category.includes(categoryItem.text)){
          return true
        }
      })
      return newItems
    }
  },
  created(){
    let notificationInfo = notificationField.find(item => item.city_code ==  this.citycode);
    if(notificationInfo.notificationCategories !== undefined){
      this.notificationCategories = notificationInfo.notificationCategories
      let hasDefaultTab = this.notificationCategories.some((item)=>item.value == 0)
      if(!hasDefaultTab){
        this.notificationCategories.unshift({text: "お知らせ", value: 0})
      }
    }
  }
}
</script>