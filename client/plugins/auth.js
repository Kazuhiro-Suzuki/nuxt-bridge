const strategy = 'refresh'

async function refreshTokenF(app, citycode, refreshToken) {
  await app.$axios
    .post('/api/v1/account/token-refresh/', { refresh_token: refreshToken })
    .then((res) => {
      // console.log(res)
      console.log('token was refreshed!')
      const bearer_token = 'Bearer ' + res.data.token
      const refreshToken = res.data.refresh_token
      app.$auth.strategy.token.set(bearer_token)
      app.$auth.strategy.refreshToken.set(refreshToken)
    })
    .catch((err) => {
      // console.log(err.response)
      console.log('refresh token was expired...')
      app.$auth.logout()
        .then(() => {
          app.router.push(`/home?citycode=${citycode}`)
          app.$notifier.showMessage({ content: 'ログアウトしました。', color: 'error' })
        })
    })
}

export default async function ({ app }) {
  app.router.afterEach((to, _) => {
    const citycode = to.query.citycode
    if (app.$auth.loggedIn) {
      // let token = app.$auth.strategy.token.get()
      let refreshToken = app.$auth.strategy.refreshToken.get()
      app.$axios
        .post('/api/v1/account/token-verify/')
        .then((res) => {
          if (citycode != res.data.city_code) {
            app.$auth.logout()
              .then(() => {
                window.location.href = `/home?citycode=${citycode}`;
              })
          }
        })
        .catch((err) => {
          // console.log(err.response)
          console.log('token was expired...')
          refreshTokenF(app, citycode, refreshToken)
        })
    }
  })
}