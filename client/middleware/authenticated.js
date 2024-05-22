export default function ({ store, redirect, route, app }) {
  if (!store.$auth.loggedIn) {
    app.$notifier.showMessage({ content: 'ログインしてください', color: 'error'})
    return redirect(`/?citycode=${route.query.citycode}`)
  }
}