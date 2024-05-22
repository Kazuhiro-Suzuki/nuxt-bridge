<template>
    <v-navigation-drawer
      class="font-weight-bold"
      style="overflow: scroll;"
      v-model="drawerData"
      :class="`${navClass} px-8`"
      :mini-variant="miniVariant"
      :clipped="clipped"
      right
      fixed
      app
      temporary
      width="332px"
    >
      
      <div class="d-flex justify-end py-4 mr-n6">
        <v-btn text @click.stop="drawer = !drawer" class="pa-0 ">
          <div class="d-flex align-center flex-column">
            <v-icon size="24px">$IconCloseLine</v-icon>
            <div style="font-size:10px;">
              閉じる
            </div>
          </div>
        </v-btn>
      </div>

      <template v-if="$auth.loggedIn">
        <v-list-item
          class="justify-start px-0 mb-3"
          @click="$router.push(`/account/profile/?citycode=${citycode}`)"
        >
          <v-row>
            <v-col cols="12" class="py-0">
              <v-list-item-avatar :color="darkColor" class="d-flex">
                <v-icon v-if="$auth.user.type === 'general'">
                  $IconThumbnailUser
                </v-icon>
                <v-icon v-else>
                  $IconThumbnailAdmin
                </v-icon>
              </v-list-item-avatar>
            </v-col>
            <v-col cols="12" class="py-0">
              <v-list-item-content class="pt-0">
                <v-list-item-title>{{ $auth.user.email }}</v-list-item-title>
                <v-list-item-subtitle class="black--text d-flex align-center">プロフィール<v-icon size="16px" color="black">$IconArrowRight</v-icon></v-list-item-subtitle>
              </v-list-item-content>
            </v-col>
          </v-row>
        </v-list-item>
      </template>

      <template v-if="!$auth.loggedIn">
        <v-list-item
          class="justify-start px-0 mb-7"
          :to="`/account?citycode=${citycode}`"
          router
          exact
          link
        >
          <v-btn 
            block
            :color="darkColor" 
            class="white--text rounded-lg py-5"
          >
            <v-list-item-content>
              <v-list-item-title>ログイン/無料会員登録</v-list-item-title>
            </v-list-item-content>
          </v-btn>
        </v-list-item>
      </template>

      <v-divider class="mr-n8" style="max-width: none"></v-divider>

      <!-- 自治体職員用メニュー -->
      <v-list v-if="$auth.loggedIn && $auth.user.type === 'business'" class="staff-list">
        <v-subheader class="pa-0">管理メニュー</v-subheader>
        <v-row dense>
          <v-col cols="4" v-for="(item, i) in staffItems" :key="i">
            <v-list-item
              class="px-0 d-block text-center"
              :to="item.to"
              router
              exact
              link
            >
              <v-icon size="40px">{{ item.icon }}</v-icon>
              <v-list-item-content class="py-1">
                <v-list-item-title class="px-2" v-text="item.title" />
              </v-list-item-content>
             </v-list-item>
          </v-col>
        </v-row>
      </v-list>

      <!-- 施設管理者用メニュー -->
      <v-list v-if="$auth.loggedIn && $auth.user.type === 'facility'" class="staff-list">
        <v-subheader class="pa-0">管理メニュー</v-subheader>
        <v-row dense>
          <v-col cols="4" v-for="(item, i) in facilityItems" :key="i">
            <v-list-item
              class="px-0 d-block text-center"
              :to="item.to"
              router
              exact
              link
            >
              <v-icon size="40px">{{ item.icon }}</v-icon>
              <v-list-item-content class="py-1">
                <v-list-item-title class="px-2" v-text="item.title" />
              </v-list-item-content>
             </v-list-item>
          </v-col>
        </v-row>
      </v-list>
      

      <v-divider></v-divider>

      <!-- 一般ユーザ用メニュー -->
      <v-list>
        <v-list-item
          class="px-0"
          v-for="(item, i) in userItems"
          :key="i"
          :to="item.to"
          router
          exact
          link
          v-if="!(item.title == 'ログイン•会員登録' && $auth.loggedIn)"
        >
          <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider v-if="$auth.loggedIn" class="mr-n8" style="max-width: none"></v-divider>

      <v-list v-if="$auth.loggedIn">
        <v-list-item 
          class="px-0"
          link
          @click="logout"
        >
            <v-list-item-icon>
              <v-icon>$IconLogoutLine</v-icon>
            </v-list-item-icon>
            <v-list-item-content class="justify-start">
              <v-list-item-title>ログアウト</v-list-item-title>
            </v-list-item-content>
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
    facilityItems: {
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
    darkColor: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      width: 'calc(33.3333% - 45px * 2/3)'
    }
  },
  computed: {
    drawerData: {
      get() {
        return this.drawer
      },
      set(val) {
        this.$emit('changeDrawer', val)
      }
    }
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

<style scoped>
.v-navigation-drawer >>> .v-navigation-drawer__content{
    overflow-y: visible;
    overflow-x: visible;
}

.v-btn >>> .v-btn__content{
  flex-direction: column;
}

.staff-list >>> .v-list-item__title {
    overflow: visible;
    white-space: normal;
    margin: 0 auto;
    /* max-width: 70px; */
}
</style>