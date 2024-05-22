<template>
  <v-container>
    <v-row class="py-6">
      <v-col cols="12">
        <mirairo-title />
      </v-col>
    </v-row>
    <v-row class="py-6">
      <h3>ミライロ連携IDの解除</h3>
      <p>
        ミライロIDとの連携を解除すると、このアプリに登録された障害者手帳の情報は全て削除されます。<br>
        手帳に基づくお知らせは届かなくなります。ご了承の上解除をお願いいたします。
      </p>
    </v-row>
    <v-row class="py-6">
      <v-col cols="12" class="d-flex justify-center">
        <v-btn
          x-large
          elevation="1"
          color="grey darken-1"
          dark
          :loading="disconnecting"
          @click="disconnect()"
        >
          連携を解除
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import MirairoTitle from "../../components/organisms/mirairo/MirairoTitle";

export default {
  components: {MirairoTitle},
  head() {
    return {
      title: 'ミライロID連携解除'
    }
  },
  data() {
    return {
      disconnecting: false
    }
  },
  computed: {
    ...mapGetters({
      regionData: 'region/getRegion',
    })
  },
  methods: {
    async disconnect() {
      this.disconnecting = true
      try {
        await this.$axios.$post('/api/v1/app/mirairo/disconnect/')
        this.$notifier.showMessage({ content: 'ミライロIDとの連携を解除しました。', color: 'info' })
        await this.$router.push({
          path: '/home',
          query: this.$route.query
        })
      } catch (e) {
        this.$notifier.showMessage({ content: '申し訳ございません、時間をおいてもう一度操作をお願いします。', color: 'error' })
      }
      this.disconnecting = false
    }
  }
}
</script>
