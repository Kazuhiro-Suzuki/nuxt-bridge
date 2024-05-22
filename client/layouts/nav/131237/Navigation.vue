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
            <v-icon :color="baseColor" size="24px">$IconCloseLine</v-icon>
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
                  $IconThumbnailUserLightBlue
                </v-icon>
                <v-icon v-else>
                  $IconThumbnailAdminLightBlue
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
              <v-list-item-title class="font-weight-bold">ログイン/無料会員登録</v-list-item-title>
            </v-list-item-content>
          </v-btn>
        </v-list-item>
      </template>

      <!-- 自治体職員用メニュー -->
      <div v-if="$auth.loggedIn && $auth.user.type === 'business'" style="background-color: #EEE;" class="over-contents">
        <v-list class="staff-list" flat>
          <v-subheader class="pa-0">管理メニュー</v-subheader>
          <v-row dense>
            <v-col cols="4" v-for="(item, i) in staffItems" :key="i">
                <v-list-item
                  class="px-0 d-block text-center white rounded-lg"
                  :to="item.to"
                  router
                  exact
                  link
                >
                  <div style="height:80px; width:80px;">
                    <div style="height: 40%; display: flex; align-items: end; justify-content: center;">
                      <v-icon :color="baseColor" size="20px">{{ item.icon }}</v-icon>
                    </div>
                    <div style="height: 60%; display: flex; align-items: end; justify-content: center;">
                      <v-list-item-content class="py-1">
                        <v-list-item-title
                          class="px-2"
                          style="font-size: 14px;"
                          v-text="item.title" />
                      </v-list-item-content>
                    </div>
                  </div>
                </v-list-item>
            </v-col>
          </v-row>
        </v-list>
      </div>


      <!-- 施設管理者用メニュー -->
      <v-list v-if="$auth.loggedIn && $auth.user.type === 'facility'" class="staff-list" flat>
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

      <div style="background-color: #EEE; height: 8px;" class="over-contents"></div>


      <!-- 一般ユーザ用メニュー -->
      <v-list flat>
          <v-list-item
            class="px-0"
            v-for="(item, i) in userItems.slice(0, 5)"
            :key="i"
            :to="item.to"
            router
            exact
            link
          >
            <v-list-item-icon>
                <v-icon :color="baseColor">{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.title" />
            </v-list-item-content>
          </v-list-item>
          
          <div style="background-color: #EEE; height: 8px;" class="over-contents"></div>

          <v-list-item
            class="px-0"
            :to="'/mirairo?citycode=131237'"
            router
            exact
            link
          >
            <v-list-item-icon>
                <v-icon :color="baseColor">$IconIdLine</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="'ミライロID'" />
            </v-list-item-content>
          </v-list-item>

          <div style="background-color: #EEE; height: 8px;" class="over-contents"></div>

          <v-list-item
            class="px-0"
            v-for="(item, i) in userItems.slice(5, 7)"
            :key="i + 100"
            :to="item.to"
            router
            exact
            link
          >
            <v-list-item-icon>
                <v-icon :color="baseColor">{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.title" />
            </v-list-item-content>
          </v-list-item>
      </v-list>

      <div v-if="$auth.loggedIn" style="background-color: #EEE; height: 8px;" class="over-contents"></div>

      <v-list v-if="$auth.loggedIn">
        <v-list-item 
          class="px-0"
          link
          @click="logout"
        >
            <v-list-item-icon>
              <v-icon :color="baseColor">$IconLogoutLine</v-icon>
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
      required: false,
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
    baseColor: {
      type: String,
      required: false,
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
.over-contents{
  margin: 0 calc(50% - 50vw);
	padding: 4px calc(50vw - 50%);
	width: 100vw;
}
</style>