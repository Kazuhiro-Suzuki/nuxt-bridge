import Cookies from 'universal-cookie'

export default function ({ $axios, redirect, error }) {
  $axios.onRequest((config) => {
    const cookies = new Cookies()
    const csrfToken = cookies.get('csrftoken')
    if (csrfToken) {
      config.headers.common['X-CSRFToken'] = csrfToken
    }
    return config
  })

	// $axios.onError((err) => {
  //   const response = err.response
  //   const config = err.config
  //   if (config.showErrorPage) {
  //     error(err)
  //   } else {
  //     return
  //   }
	// })

}
