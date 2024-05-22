export const state = () => ({
  regionData: null,
  errorMessage: '',
})

export const mutations = {
  setRegionData(state, value) {
    state.regionData = value
  },
  setErrorMessage(state, value) {
    state.errorMessage = value
  },
}

export const getters = {
  getRegion: state => {
    return state.regionData
  },
  getErrorMessage: state => {
    return state.errorMessage
  },
}

export const actions = {
  async getRegionData({ commit, state }, { citycode }) {
    // すでに取得済みならなにもしない（home以外でもこのアクションを呼ぶため）
    if (state.regionData) return;
    const region = await this.$api.getRegion(`city_code=${ citycode }`)
    // console.log(region)
    if (region.status == 200) {
      commit('setRegionData', region.data)
    } else {
      if (region.data.detail) {
        commit('setErrorMessage', region.data.detail)
      } else {
        commit('setErrorMessage', 'サーバエラーです、時間をおいてお試しください。')
      }
    }
  },
  async setErrorMessage({ commit }, { message }) {
    commit('setErrorMessage', message)
  },
}
