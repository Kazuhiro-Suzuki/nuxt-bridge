<template>
  <v-card v-if="Object.keys(slotItems).length !== 0" elevation="0">
    <v-card-title class="justify-center">
      <div>{{ month }}月</div>
    </v-card-title>
    <v-card-text>
      <v-simple-table>
        <thead>
          <tr>
            <th>
              <NormalMiniButton
                :color="`${regionItem.base_color} lighten-4`"
                text="＜"
                :disabled="!isWeekBtn"
                @clickAction="lastWeek"
              />
            </th>
            <th class="text-center" style="white-space: nowrap;" v-for="(slot, i) in slotItems['keys']">
              {{ slot }}
            </th>
            <th>
              <NormalMiniButton
                :color="`${regionItem.base_color} lighten-4`"
                text="＞"
                @clickAction="nextWeek"
              />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(division, i) in slotItems['divisions']">
            <td>{{ i }}</td>
            <td class="text-center" v-for="(slot, j) in slotItems['keys']">
              <NormalMiniButton
                v-if="isSlotButtonValid(division, slot)"
                :color="slotColor(division, slot)"
                :text="division[slot]['mark']"
                :disabled="disabled(division[slot])"
                @clickAction="selectSlot(division[slot]['id'])"
              />
              <div v-else class="text-center">―</div>
            </td>
          </tr>
        </tbody>
      </v-simple-table>
    </v-card-text>
    <v-card-actions>
      <v-spacer/>
      <NormalButton
        color="grey lighten-2"
        text="戻 る"
        @clickAction="$router.push(`/reservation?citycode=${$route.query.citycode}`)"
      />
      <NormalButton
        color="grey lighten-2"
        text="次 へ"
        :disabled="slotId.length == 0 || slotId.length > facilityItem.maxAppointmentsCount"
        @clickAction="$router.push({
            path: '/reservation/confirm',
            query: {
              citycode: regionItem.city_code,
              facilityId: facilityItem.id,
              slotId: slotId.join(','),
            }
          })"
      />
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      weekCount: 0,
      isWeekBtn: false,
      slotId: []
    }
  },
  async created() {
    if (!this.$auth.loggedIn) {
      this.$router.push(`/account?citycode=${this.$route.query.citycode}`)
    }
  },
  props: {
    regionItem: {
      type: Object,
      required: true
    },
    facilityItem: {
      type: Object,
      required: true
    },
    slotItems: {
      type: Object,
      required: true
    }
  },
  computed: {
    month () {
      let months = []
      this.slotItems['keys'].forEach(date => {
        months.push(date.split('月')[0])
      })
      months = [...new Set(months)]
      return months.join('月/')
    }
  },
  methods: {
    lastWeek() {
      this.weekCount -= 1
      if (this.weekCount <= 0) {
        this.isWeekBtn = false
      }
      this.$store.dispatch('slot/getSlotData', { facilityId: this.facilityItem.id, citycode: this.regionItem.city_code, weekCount: this.weekCount })
    },
    nextWeek() {
      this.weekCount += 1
      if (this.weekCount > 0) {
        this.isWeekBtn = true
      }
      this.$store.dispatch('slot/getSlotData', { facilityId: this.facilityItem.id, citycode: this.regionItem.city_code, weekCount: this.weekCount })
    },
    isSlotButtonValid(division, key) {
      return key in division && division[key]['mark'] !== '―'
    },
    slotColor(division, slot){
      if(this.regionItem.city_code == "131032"){
        if(this.slotId.includes(division[slot]['id'])){
          return `${this.regionItem.base_color} lighten-2`
        }else{
          return `${this.regionItem.base_color} lighten-4`
        }
      }
      if(this.regionItem.city_code == "142077"){
        if(this.slotId.includes(division[slot]['id'])){
          return `${this.regionItem.dark_color}`
        }else{
          return `${this.regionItem.base_color}`
        }
      }
    },
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
    selectSlot(id){
      if(this.slotId.includes(id)){
        this.slotId = this.slotId.filter(item => item !== id)
        return true
      }
      if(this.slotId.length < this.facilityItem.maxAppointmentsCount){
        this.slotId.push(id);
        return true
      }
      this.$notifier.showMessage({ content: `${this.facilityItem.maxAppointmentsCount}枠までしか同時に予約できません。`, color: 'info' });
    }
  },
}
</script>
