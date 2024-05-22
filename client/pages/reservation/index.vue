<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" v-if="['131032'].includes(citycode)">
        <v-container>
          <v-row justify="center">
            <v-col sm="10" md="8" lg="8" xl="8">
              <v-card>
                <v-card-text>
                  <v-list-item class="pl-0 pr-0">
                    <v-list-item-avatar class="mt-0 mb-0 mr-0">
                      <v-icon>mdi-circle-small</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content class="subtitle-1" style="display: inline">
                      短期入所の予約について、令和6年3月1日以降、LINEでの利用申請に移行いたします。令和6年3月1日以降は、本アプリから予約することはできませんので、ご注意ください。
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item class="pl-0 pr-0">
                    <v-list-item-avatar class="mt-0 mb-0 mr-0">
                      <v-icon>mdi-circle-small</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content class="subtitle-1" style="display: inline">
                      LINEでの予約には、事前に新たな登録が必要です。まず、LINE港区公式アカウントを友達登録し、障害者短期入所の登録を行ってください。<br />
                      港区公式アカウントは、LINEを起動後、メニュー「ホーム」の「友だち追加」画面で「検索」を選択し、「@minatocity」と入力して検索してください。<br />
                      ※LINE該当ページ（<a href="https://line.me/R/ti/p/%40805rxtco#~" style="display: contents;">https://line.me/R/ti/p/%40805rxtco#~</a>）<br />
                      ※詳細な説明はこちら（<a href="https://d1cy8kr2yj0xug.cloudfront.net/temp-notice/reservation.pdf" style="display: contents;">PDF</a>）
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item class="pl-0 pr-0">
                    <v-list-item-avatar class="mt-0 mb-0 mr-0">
                      <v-icon>mdi-circle-small</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content class="subtitle-1" style="display: inline">
                      各施設の移行スケジュールは、以下の通りです。<br />
                      障害保健福祉センター 令和6年3月1日（5月分予約）に移行<br />
                      支援ホーム南麻布 令和6年4月1日に移行予定<br />
                      精神障害者支援センター 令和6年4月1日に移行予定
                    </v-list-item-content>
                  </v-list-item>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-col>
      <v-col
        cols="12"
        xs="10"
        sm="10"
        md="10"
        lg="10"
        v-if="['142077'].includes(citycode)"
      >
        <ReservationHome
          :baseColor="regionData.base_color"
          :darkColor="regionData.dark_color"
          :title="title"
          :isMaintenance="isMaintenance"
          :items="items"
          :facilityItems="facilityItems"
          :citycode="citycode"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  head() {
    return {
      title: this.title,
    };
  },
  data() {
    return {
      citycode: this.$route.query.citycode,
    };
  },
  async asyncData({ route, $api }) {
    let title = "";
    let items = [];
    let facilityItems = [];
    let errorMessage = "";
    let isMaintenance = false;

    const reservationResponse = await $api.getReservationConnection(
      `city_code=${route.query.citycode}`
    );
    if (reservationResponse.status == 200) {
      isMaintenance = !reservationResponse.data.is_active;
      title = reservationResponse.data.title + " 予約";
      reservationResponse.data.messages.forEach((item) => {
        items.push({ text: item });
      });
    } else {
      errorMessage = "サーバーエラーです、時間置いてからお試しください。";
    }

    if(isMaintenance){
      return {
        facilityItems: [],
        errorMessage: "",
        isMaintenance: isMaintenance,
        title: title,
        items: [],
      };
    }

    const response = await $api.getReservationFacility(
      `city_code=${route.query.citycode}`
    );
    if (response.status === 200) {
      facilityItems = response.data;
    } else {
      if (response.data.detail) {
        errorMessage = response.data.detail;
      } else {
        errorMessage = "サーバーエラーです、時間置いてからお試しください。";
      }
    }
    return {
      facilityItems,
      errorMessage,
      isMaintenance,
      title,
      items,
    };
  },
  computed: {
    ...mapGetters({
      regionData: "region/getRegion",
    }),
  },
};
</script>
