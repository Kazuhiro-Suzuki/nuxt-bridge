<template>
  <v-container>
    <div  v-if="!isMaintenance">
      <v-row justify="center" class="pb-14">
        <v-col cols="12">
            <div class="justify-center text-md-h4 text-h5 font-weight-bold">
                {{ title }}
            </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="12" md="3" lg="3" xl="3">
          <MainMenuButton
              title="予約履歴はこちら"
              :to="`/history?citycode=${citycode}`"
              :color="darkColor"
              imgFile=''
              :outlined="true"
              BtnClass="rounded-lg"
          />
        </v-col>
      </v-row>
      <v-row class="pb-5">
        <v-col cols="12">
          <v-list-item
            dense
            class="pl-0 pr-0"
            v-for="(item, i) in items"
            :key="i"
          >
            <v-list-item-avatar class="ma-0">
              <v-icon>mdi-circle-small</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
                {{ item.text }}
            </v-list-item-content>
          </v-list-item>
        </v-col>
      </v-row>
        <v-col
          cols="12"
          v-for="(item, i) in facilityItems"
          :key=i
        >
          <v-card class="rounded-lg pa-5">
            <ReservationFacilityInfo2
              :facilityItem="item"
            />
            <v-divider class="pb-5"/>
            <v-card-actions class="justify-center">
              <NormalButton
                block
                text="予約する"
                :class="`${baseColor} lighten-4 white--text`"
                :color="`${darkColor}`"
                :disabled="(!$auth.loggedIn || $auth.user.type !== 'general')"
                @clickAction="$router.push(`/reservation/list?citycode=${item.cityCode}&facilityId=${item.id}`)"
              />
            </v-card-actions>
          </v-card>
        </v-col>
    </div>
    <v-card v-else>
      <v-card-text >
        <p class="text-h6" style="color:red">只今、{{ title }}はメンテナンス中です。今しばらくお待ちください。</p>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  props: {
    baseColor: {
      type: String,
      required: true,
    },
    darkColor: {
      type: String,
      required: true,
    },
    citycode: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    facilityItems: {
      type: Array,
      required: true,
    },
    items: {
      type: Array,
      required: true,
    },
    isMaintenance: {
      type: Boolean,
      required: true,
    },
  },
}
</script>
