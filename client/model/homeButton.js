export const homeButton = [
  {
    city_name: 'minato_city',
    city_code: '131032',
    mainButtons: [
      {
        title: 'ログイン•会員登録',
        to: `/account?citycode=131032`,
        imgFile: 'v.png',
        type: '',
      },
      {
        title: '障害者手帳情報（ミライロID）',
        to: `/mirairo?citycode=131032`,
        imgFile: 'common/image-mirairo-id.png',
        type: '',
      },
      {
        title: '障害者のためのサービス一覧',
        to: '/information?citycode=131032',
        imgFile: 'common/image-servicelist.png',
        type: '',
      },
      {
        title: '障害者施設 一覧',
        to: `/facility?citycode=131032`,
        imgFile: 'common/list-2389219_640.png',
        type: '',
      },
      {
        title: '短期入所施設 予約',
        to: `/reservation?citycode=131032`,
        imgFile: 'common/image-search.png',
        type: '',
      },
      // {
      //   title: '短期入所施設 予約履歴',
      //   to: `/history?citycode=131032`,
      //   imgFile: 'common/image-building.png',
      //   type: '',
      // },
      {
        title: 'よくある質問',
        to: `/faq?citycode=131032`,
        imgFile: 'common/image-comment.png',
        type: '',
      },
    ],
    subButtons: [],
  },
  {
    city_name: 'chigasaki',
    city_code: '142077',
    mainButtons: [
      {
        title: '障がい福祉のあんない',
        to: `/booklet?citycode=142077`,
        imgFile: '',
        icon:'$IconBooklet2t',
        type: '',
      },
      {
        title: '事業者一覧・空き状況',
        to: `/congestion?citycode=142077`,
        imgFile: '',
        icon:'$IconFacility2t',
        type: '',
      },
      {
        title: 'オンライン相談予約',
        to: `/reservation?citycode=142077`,
        imgFile: '',
        icon:'$IconConsultation2t',
        type: '',
      },
      {
        title: 'やさしいマップちがさき',
        to: `/barrier-free-map?citycode=142077`,
        imgFile: '',
        icon:'$IconBarrierFreeMap2t',
        type: '',
      },
    ],
    subButtons: [
      {
        title: '障がい者手帳アプリ ミライロID',
        to: `/mirairo?citycode=142077`,
        imgFile: 'common/image-mirairo-id.png',
        icon:'',
        type: '',
      },
      {
        title: 'お問い合わせ・よくある質問',
        to: `/faq?citycode=142077`,
        imgFile: '',
        icon: '$IconHelpColor2t',
        type: '',
      },
    ],
  },
  {
    city_name: 'edogawa',
    city_code: '131237',
    mainButtons: [
      {
        title: '障害者福祉のしおり',
        to: `/booklet?citycode=131237`,
        imgFile: '',
        icon:'$IconBooklet2tLightBlue',
        type: '',
      },
      {
        title: '事業者一覧',
        to: `/congestion?citycode=131237`,
        imgFile: '',
        icon:'$IconFacility2tLightBlue',
        type: '',
      },
    ],
    subButtons: [
      {
        title: '障がい者手帳アプリ ミライロID',
        to: `/mirairo?citycode=131237`,
        imgFile: 'common/image-mirairo-id.png',
        icon:'',
        type: '',
      },
      {
        title: 'お問い合わせ・よくある質問',
        to: `/faq?citycode=131237`,
        imgFile: '',
        icon: '$IconHelpColor2tLightBlue',
        type: '',
      },
    ],
  },
  {
    city_name: 'hida',
    city_code: '212172',
    mainButtons: [
      {
        title: '障がい者支援情報',
        to: `/booklet?citycode=212172`,
        imgFile: 'common/img-booklet-green-dark.svg',
        icon:'$IconBooklet2tDarkGreen',
        type: '',
      },
      {
        title: '各種相談窓口',
        to: `/information?citycode=212172`,
        imgFile: 'common/img-support-green-dark.svg',
        icon:'$IconSupport2t',
        type: '',
      }
    ],
    subButtons: [
      {
        title: '障がい福祉情報',
        to: `https://www.city.hida.gifu.jp/site/sougouhukusi/44031.html`,
        imgFile: '',
        icon:'$IconService2t',
        type: 'href',
      },
      {
        title: 'ミライロID',
        to: `/mirairo?citycode=212172`,
        imgFile: 'common/image-mirairo-id.png',
        icon:'',
        type: '',
      },
      {
        title: 'よくある質問',
        to: `/faq?citycode=212172`,
        imgFile: '',
        icon: '$IconHelp2t',
        type: '',
      },
    ],
  },
  {
    city_name: 'nasushiobara',
    city_code: '092134',
    mainButtons: [
      {
        title: '事業所一覧',
        to: `/congestion?citycode=092134`,
        imgFile: '',
        icon:'$IconFacility2tHex118C46',
        type: '',
      },
      {
        title: 'るぴなすノート',
        to: `/support-file/start?citycode=092134`,
        imgFile: '',
        icon:'$IconBooklet2tHex118C46',
        type: '',
      }
    ],
    subButtons: [
      {
        title: '障害者支援情報',
        to: `/booklet?citycode=092134`,
        imgFile: '',
        icon:'$IconService2tHex118C46',
        type: '',
      },
      {
        title: 'ミライロID',
        to: `/mirairo?citycode=092134`,
        imgFile: 'common/image-mirairo-id.png',
        icon:'',
        type: '',
      },
      {
        title: 'よくある質問',
        to: `/faq?citycode=092134`,
        imgFile: '',
        icon: '$IconHelp2tHex118C46',
        type: '',
      },
    ],
  },
]