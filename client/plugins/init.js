export default async ({ store, route }) => {
  // 初期化処理

  // 自治体プロファイルの取得（サイトデザインに必要なため必ず呼び出す）
  await store.dispatch('region/getRegionData', { citycode: route.query.citycode })
}
