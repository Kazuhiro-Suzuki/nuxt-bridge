export default ({ store, route }) => {
    const backValue = route.meta[0]?.back
    const canBack = !!backValue
    const backTo = backValue === true ? null : backValue
    store.commit('back/changeBack', { canBack, backTo })
  }