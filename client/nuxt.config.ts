import colors from 'vuetify/es5/util/colors'
import { defineNuxtConfig } from '@nuxt/bridge'
import { type Configuration } from 'webpack'
import * as dotenv from 'dotenv'
dotenv.config()

export default defineNuxtConfig({
  bridge: {
    capi: true,
    typescript: true,
    nitro: false // If migration to Nitro is complete, set to true
  },

  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - 障害者支援アプリ',
    title: '障害者支援アプリ',
    htmlAttrs: {
      lang: 'ja'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@toast-ui/editor/dist/toastui-editor.css',
    '@toast-ui/editor/dist/toastui-editor-viewer.css',
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '~/plugins/notifier' },
    { src: '~/plugins/components' },
    { src: '~/plugins/validationRules' },
    { src: '~/plugins/axios' },
    { src: '~/plugins/api' },
    { src: '~/plugins/init' },
    { src: '~/plugins/vue-ctk-date-time-picker.js', mode: 'client', ssr: false },
  ],

  /*
   ** Router configuration
   */
  router: {
    middleware: ['back']
  },

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    '@nuxtjs/vuetify',
    '@nuxtjs/device',
    '@nuxtjs/svg',
    '@nuxtjs/dotenv',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    ['@nuxtjs/moment', ['ja']],
    ['@nuxtjs/google-gtag', {
      id: process.env.PUBLIC_GTAG_ID,
      debug: true,
    }]
  ],

  // axios settings
  axios: {
    proxy: true,
    credentials: true,
  },
  proxy: {
    '/api/v1': {
      target: process.env.BASE_URL
    }
  },

  // auth settings
  auth: {
    localStorage: false,
    strategies: {
      refresh: {
        // scheme: 'local',
        scheme: 'refresh',
        token: {
          property: 'token',
          global: true,
          // maxAge: 1800,
        },
        refreshToken: {
          property: 'refresh_token',
          data: 'refresh_token',
          // maxAge: 60 * 60 * 24 * 30
        },
        user: {
          property: 'user',
        },
        endpoints: {
          login: { url: '/api/v1/account/token-obtain/', method: 'post' },
          // refresh: { url: '/api/v1/account/token-refresh/', method: 'post' },
          user: { url: '/api/v1/account/user/', method: 'get' },
          logout: false,
        }
      }
    },
    plugins: ['~/plugins/axios.js', { src: '~/plugins/auth.js', mode: 'client' }],
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    treeShake: true,
    optionsPath: './vuetify.options.js',
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        }
      }
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    extend(config: Configuration) {
      config.module?.rules.push({
        test: /\.[cm]?js$/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      })
    },
  },
})
