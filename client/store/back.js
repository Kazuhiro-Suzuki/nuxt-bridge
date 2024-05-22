export const state = () => ({
    canBack: false,
    backTo: null,
  })
  
  export const mutations = {
    changeBack(state, { canBack, backTo }) {
      state.canBack = canBack
      state.backTo = backTo
    },
  }