<template>
    <v-navigation-drawer
      v-model="drawer"
      :class="navClass"
      :mini-variant="miniVariant"
      :clipped="clipped"
      right
      fixed
      app
    >

      <template v-slot:prepend v-if="$auth.loggedIn">
        <v-list-item
          two-line
          class="ma-2"
          @click="$router.push(`/account/profile/?citycode=${citycode}`)"
        >
          <v-list-item-avatar class="white">
            <v-icon v-if="$auth.user.type === 'general'">
              mdi-account
            </v-icon>
            <v-icon v-else>
              mdi-account-alert
            </v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ $auth.user.email }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>

      <v-divider></v-divider>

      <!-- 自治体職員用メニュー -->
      <v-list v-if="$auth.loggedIn && $auth.user.type === 'business'">
        <v-list-item
          v-for="(item, i) in staffItems"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-btn block class="ma-2 white">
            <v-list-item-action class="ma-2">
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title v-text="item.title" />
            </v-list-item-content>
          </v-btn>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <!-- 一般ユーザ用メニュー -->
      <v-list>
        <v-list-item
          v-for="(item, i) in userItems"
          :key="i"
          :to="item.to"
          router
          exact
          link
          v-if="!(item.title == 'ログイン•会員登録' && $auth.loggedIn)"
        >
          <v-btn
            block
            class="ma-2 white"
          >
            <v-list-item-action class="ma-2">
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title v-text="item.title" />
            </v-list-item-content>
          </v-btn>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list v-if="$auth.loggedIn">
        <v-list-item>
          <v-btn block dark class="ma-2" @click="logout">
            <v-list-item-action class="ma-2">
              <v-icon>mdi-logout</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>ログアウト</v-list-item-title>
            </v-list-item-content>
          </v-btn>
        </v-list-item>
      </v-list>

    </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    miniVariant: {
      type: Boolean,
      required: true,
    },
    staffItems: {
      type: Array,
      required: true,
    },
    userItems: {
      type: Array,
      required: true,
    },
    clipped: {
      type: Boolean,
      required: true,
    },
    fixed: {
      type: Boolean,
      required: true,
    },
    navClass: {
      type: String,
      required: true,
    },
    citycode: {
      type: String,
      required: true,
    },
    drawer: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    logout() {
      this.$auth.logout()
        .then(() => {
          this.$router.push(`/?citycode=${this.citycode}`)
          this.$notifier.showMessage({ content: 'ログアウトしました。', color: 'info' })
        })
    },
  },
}
</script>