<template>
  <v-card elevation="0">
    <v-card-title class="text-h6" style="white-space: pre-line">{{ facilityItem.name }}</v-card-title>
    <v-card-subtitle>
      {{ facilityItem.business_description }}
    </v-card-subtitle>
    <v-card-text>
      <v-row>
        <v-col>
          <div class="font-weight-bold">電話</div>
          <div class="px-1">{{ facilityItem.phone_number }}</div>
          <div class="font-weight-bold">FAX</div>
          <div class="px-1">{{ facilityItem.fax_number ? facilityItem.fax_number : "-"}}</div>
          <!--- 障害者施設 --->
          <!--  知的 -->
          <div v-if="isDisabledFacility && facilityItem.category=='2'">
            <div class="font-weight-bold">住所</div>
            <div class="px-1">{{ facilityItem.address }}</div>
            <div v-if="isDisplayCapacity(facilityItem)">
              <div class="font-weight-bold">定員</div>
              <div class="px-1">{{ facilityItem.capacity }}人</div>
            </div>
          </div>
          <!--  精神 -->
          <div v-else-if="isDisabledFacility && facilityItem.category=='1'">
            <div v-if="isDisplayCapacity(facilityItem)">
              <div class="font-weight-bold">定員</div>
              <div class="px-1">{{ facilityItem.capacity }}人</div>
            </div>
          </div>
          <!--  短期入所 -->
          <div v-else-if="isDisabledFacility && facilityItem.category=='3'">
            <div class="font-weight-bold">住所</div>
            <div class="px-1">{{ facilityItem.address }}</div>
            <div v-if="isDisplayCapacity(facilityItem)">
              <div class="font-weight-bold">定員</div>
              <div class="px-1">{{ facilityItem.capacity }}人</div>
            </div>
          </div>
          <!--  その他 -->
          <div v-else-if="isDisabledFacility && facilityItem.category=='5'">
            <div class="font-weight-bold">住所</div>
            <div class="px-1">{{ facilityItem.address }}</div>
            <div class="font-weight-bold">問い合わせ</div>
            <div class="px-1">{{ facilityItem.contact }}</div>
            <div class="font-weight-bold">仕事の内容</div>
            <div class="px-1">{{ facilityItem.contents }}</div>
            <div class="font-weight-bold">対象者</div>
            <div class="px-1">{{ facilityItem.target }}</div>
          </div>
          <!-- 相談窓口 -->
          <div v-else-if="facilityItem.facility_type=='consultation_service'">
            <div class="font-weight-bold">住所</div>
            <div class="px-1">{{ facilityItem.address }}</div>
            <div class="font-weight-bold">問い合わせ窓口</div>
            <div class="px-1">{{ facilityItem.contact }}</div>
            <div class="font-weight-bold">内容等</div>
            <div class="px-1" style="white-space: pre-line">{{ facilityItem.contents }}</div>
          </div>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-row justify="center">
        <v-col cols="6">
          <div v-if="facilityItem.google_map">
            <NormalButton
              color="grey lighten-2"
              text="地 図"
              @clickAction="map"
              :block="block"
            />
          </div>
        </v-col>
        <v-col cols="6">
          <div v-if="facilityItem.phone_number">
            <NormalButton
              color="grey lighten-2"
              text="電 話"
              @clickAction="tel"
              :block="block"
            />
          </div>
        </v-col>
      </v-row>
    </v-card-actions>
    <v-card-actions>
      <v-spacer></v-spacer>
      <NormalButton
        color="grey lighten-2"
        text="戻 る"
        @clickAction="$router.go(-1)"
      />
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    baseColor: {
      type: String,
      required: true
    },
    cityCode: {
      type: String,
      required: true
    },
    facilityItem: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      block: true,
    }
  },
  methods: {
    tel() {
      window.location.href = `tel:${this.facilityItem.phone_number}`
    },
    homePage() {
      window.open(this.facilityItem.homepage, '_blank')
    },
    map() {
      window.open(this.facilityItem.google_map, '_blank')
    },
    isDisabledFacility(){
      return function(facilityItem){
        if(facilityItem.facility_type=='disabled_facility'){
          return true
        }
        return false
      }
    },
    isDisplayCapacity(facilityItem){
      if(facilityItem.capacity && facilityItem.capacity !== '0'){
          return true
        }
        return false
    }
  },
}
</script>
