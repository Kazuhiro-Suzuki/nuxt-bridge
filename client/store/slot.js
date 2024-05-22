export const state = () => ({
  slotData: {},
})

export const mutations = {
  setSlotData(state, value) {
    state.slotData = value
  }
}

export const getters = {
  getSlot: state => {
    return state.slotData
  },
}

export const actions = {
  async getSlotData({ commit }, data) {
    const response = await this.$api.postCustomizeSlot(data)
    if (response.status === 200) {
      commit('setSlotData', response.data)
    } else {
      if (response.data.detail) {
        commit('region/setErrorMessage', response.data.detail, { root: true })
      } else {
        commit('region/setErrorMessage', 'サーバエラーです、時間をおいてお試しください。', { root: true })
      }
    }
  }
}
