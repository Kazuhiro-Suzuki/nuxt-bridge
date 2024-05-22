export const state = () => ({
  facilitiesData: [],
  facilityData: {},
})

export const mutations = {
  setFacilitiesData(state, value) {
    state.facilitiesData = value
  },
  setFacilityData(state, value) {
    state.facilityData = value
  },
}

export const getters = {
  getFacilities: state => {
    return state.facilitiesData
  },
  getFacility: state => {
    return state.facilityData
  },
}

export const actions = {
  async getFacilitiesData({ commit }, { citycode }) {
    const response = await this.$api.getReservationFacility(`city_code=${citycode}`)
    if (response.status === 200) {
      commit('setFacilitiesData', response.data)
    } else {
      if (response.data.detail) {
        commit('region/setErrorMessage', response.data.detail, { root: true })
      } else {
        commit('region/setErrorMessage', 'サーバエラーです、時間をおいてお試しください。', { root: true })
      }
    }
  },
  async getFacilityData({ commit }, { facilityId, citycode }) {
    const response = await this.$api.getReservationFacilityDetail(`city_code=${citycode}&facilityId=${ facilityId }`)
    if (response.status === 200) {
      commit('setFacilityData', response.data)
    } else {
      if (response.data.detail) {
        commit('region/setErrorMessage', response.data.detail, { root: true })
      } else {
        commit('region/setErrorMessage', 'サーバエラーです、時間をおいてお試しください。', { root: true })
      }
    }
  },
}
