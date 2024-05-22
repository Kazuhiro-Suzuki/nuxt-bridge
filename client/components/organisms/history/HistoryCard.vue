<template>
  <v-card>
    <DenseToolBar
      :baseColor="baseColor"
      :title="title">
    </DenseToolBar>
    <v-card-text>
      <v-row>
        <v-col cols="12" v-for="(item, index) in viewList" :key="index">
          <v-card>
            <v-card-title clas="text-h6">
              {{ facilityData[slotData[String(item['slotId'])]['facilityId']]['displayName'] }}
            </v-card-title>
            <v-card-text>
              <div class="font-weight-bold">住所</div>
              {{ facilityData[slotData[String(item['slotId'])]['facilityId']]['address'] }}
              <div class="font-weight-bold">電話</div>
              {{ facilityData[slotData[String(item['slotId'])]['facilityId']]['phoneNumber'] }}
              <div class="font-weight-bold">予約枠</div>
              {{ slotData[String(item['slotId'])]['date'] }}　{{ slotData[String(item['slotId'])]['division'] }}
            </v-card-text>
            <v-card-actions>
              <v-spacer/>
              <NormalButton
                :color="`${baseColor} lighten-4`"
                text="キャンセル"
                :disabled="disabled(slotData[String(item['slotId'])])"
                @clickAction="confirmCancel(item['id'])"
              />
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>

    <div class="text-center">
      <v-pagination
        v-model="currentNumberPage"
        :length="totalPageCount"
        :color="`${baseColor}`"
      />
    </div>

    <v-dialog
      v-model="deleteDialog"
      width="400"
    >
      <Confirmation
        buttonText="キャンセルする"
        :baseColor="baseColor"
        title="キャンセル確認"
        @clickEvent2="doCancel"
      />
    </v-dialog>

  </v-card>
</template>

<script>
export default {
  data() {
    return {
      currentNumberPage: 1,
      totalPageCount: 0,
      recordCount: 5,
      currentReservations: [],
      deleteDialog: false,
      cancelId: '',
    }
  },
  props: {
    baseColor: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    reservations: {
      type: Array,
      required: true,
    },
    slotData: {
      type: Object,
      required: true,
    },
    facilityData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    viewList() {
      this.totalPageCount = Math.ceil(this.reservations.length / this.recordCount)
      return this.reservations.slice((this.currentNumberPage - 1) * this.recordCount, this.currentNumberPage * this.recordCount)
    },
  },
  methods: {
    disabled(slotObj) {
      const openAt = Date.parse(slotObj['openAt'])
      const closeAt = Date.parse(slotObj['closeAt'])
      if (!isNaN(openAt) && !isNaN(closeAt)) {
        if (openAt < Date.now() && Date.now() < closeAt) {
          return false
        }
      }
      return true
    },
    confirmCancel(id) {
      this.cancelId = id
      this.deleteDialog = true
    },
    async doCancel() {
      this.deleteDialog = false
      const response = await this.$api.cancelReservation(this.cancelId, { email: this.$auth.user.email })
      if (response.status === 200) {
        this.$notifier.showMessage({ content: 'キャンセルしました。', color: 'info' })
      } else {
        this.$notifier.showMessage({ content: 'キャンセルできませんでした。', color: 'error' })
      }
      this.$nuxt.refresh()
    },
  },
}
</script>
