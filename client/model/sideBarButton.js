export const sideBarButton = [
  {
    city_name: 'minato_city',
    city_code: '131032',
    staffItems: [
      {
        title: 'お知らせ管理',
        icon: 'mdi-comment-text',
        to: `/admin/notification?citycode=131032`,
      },
      {
        title: 'ユーザー管理',
        icon: 'mdi-account',
        to: `/admin/account/list?citycode=131032`,
      },
      {
        title: 'お問い合わせ管理',
        icon: 'mdi-message-question-outline',
        to: `/admin/faq/list?citycode=131032`,
      },
      // {
      //   title: '施設情報管理',
      //   icon: 'mdi-hospital-building',
      //   to: `/admin/facility?citycode=`,
      // },
    ],
    userItems: [
      {
        title: 'お知らせ一覧',
        icon: 'mdi-alert-circle',
        to: '/notification?citycode=131032',
      },
      {
        title: 'ログイン•会員登録',
        icon: 'mdi-account',
        to: '/account?citycode=131032',
      },
      {
        title: 'ミライロID',
        icon: 'mdi-note',
        to: '/mirairo?citycode=131032',
      },
      {
        title: 'サービス一覧',
        icon: 'mdi-format-list-text',
        to: '/information?citycode=131032',
      },
      {
        title: '障害者施設 一覧',
        icon: 'mdi-clipboard-list',
        to: '/facility?citycode=131032',
      },
      {
        title: '短期入所 予約',
        icon: 'mdi-hospital-building',
        to: '/reservation?citycode=131032',
      },
      // {
      //   title: '短期入所 予約履歴',
      //   icon: 'mdi-history',
      //   to: '/history?citycode=131032',
      // },
      {
        title: 'よくある質問',
        icon: 'mdi-cloud-question',
        to: '/faq?citycode=131032',
      },
      {
        title: '利用規約',
        icon: 'mdi-clipboard-text',
        to: '/termofservice?citycode=131032',
      },
    ],
    facilityItems: [],
  },
  {
    city_name: 'chigasaki',
    city_code: '142077',
    staffItems: [
      {
        title: 'お知らせ管理',
        icon: '$IconSettingNotificationLine',
        to: `/admin/notification?citycode=142077`,
      },
      {
        title: 'お問合せ管理',
        icon: '$IconSettingInquiryLine',
        to: `/admin/faq/list?citycode=142077`,
      },
      {
        title: 'ユーザー管理',
        icon: '$IconSettingUserLine',
        to: `/admin/account/list?citycode=142077`,
      },
      {
        title: '施設ユーザー管理',
        icon: '$IconSettingOfficeuserLine',
        to: `/admin/facility/user?citycode=142077`,
      },
      {
        title: 'アンケート管理',
        icon: '$IconSurveyLine',
        to: '/admin/survey?citycode=142077',
      },
      {
        title: 'Slack管理',
        icon: '$IconSlack',
        to: '/admin/slack?citycode=142077',
      },
      {
        title: '施設管理',
        icon: '$IconSettingOfficeLine',
        to: '/admin/facility?citycode=142077',
      },
    ],
    userItems: [
      {
        title: 'お知らせ',
        icon: '$IconInformationLine',
        to: '/notification?citycode=142077',
      },
      {
        title: '事業者一覧・空き状況',
        icon: '$IconFacilityLine',
        to: '/congestion?citycode=142077',
      },
      {
        title: 'やさしいマップちがさき',
        icon: '$IconBarrierFreeMapLine',
        to: '/barrier-free-map?citycode=142077',
      },
      {
        title: '障がい福祉のあんない',
        icon: '$IconBookletLine',
        to: '/booklet?citycode=142077',
      },
      {
        title: 'オンライン相談予約',
        icon: '$IconConsultationLine',
        to: '/reservation?citycode=142077',
      },
      {
        title: '手話通訳者・要約筆記者の派遣',
        icon: '$IconRequestLine',
        to: '/information?citycode=142077',
      },
      {
        title: 'ミライロID',
        icon: '$IconIdLine',
        to: '/mirairo?citycode=142077',
      },
      {
        title: 'お問い合わせ・よくある質問',
        icon: '$IconQuestionLine',
        to: '/faq?citycode=142077',
      },
      {
        title: '利用規約',
        icon: '$IconTermsLine',
        to: '/termofservice?citycode=142077',
      },
    ],
    facilityItems: [
      {
        title: 'Slack管理',
        icon: '$IconSlack',
        to: '/admin/slack?citycode=142077',
      },
    ],
  },
  {
    city_name: 'edogawa',
    city_code: '131237',
    staffItems: [
      {
        title: 'お知らせ管理',
        icon: '$IconSettingNotificationLine',
        to: `/admin/notification?citycode=131237`,
      },
      {
        title: 'ユーザー管理',
        icon: '$IconSettingUserLine',
        to: `/admin/account/list?citycode=131237`,
      },
      {
        title: '施設ユーザー管理',
        icon: '$IconSettingOfficeuserLine',
        to: `/admin/facility/user?citycode=131237`,
      },
      {
        title: '施設管理',
        icon: '$IconSettingOfficeLine',
        to: '/admin/facility?citycode=131237',
      },
    ],
    userItems: [
      {
        title: 'ホーム',
        icon: '$IconHomeLine',
        to: '/home?citycode=131237',
      },
      {
        title: 'お知らせ',
        icon: '$IconInformationLine',
        to: '/notification?citycode=131237',
      },
      {
        title: 'ヘルプカード',
        icon: '$IconRequestLine',
        to: '/help-card?citycode=131237',
      },
      {
        title: '障害者福祉のしおり',
        icon: '$IconBookletLine',
        to: '/booklet?citycode=131237',
      },
      {
        title: '事業者一覧',
        icon: '$IconFacilityLine',
        to: '/congestion?citycode=131237',
      },
      // {
      //   title: 'ミライロID',
      //   icon: '$IconIdLine',
      //   to: '/mirairo?citycode=131237',
      // },
      {
        title: 'お問い合わせ・よくある質問',
        icon: '$IconQuestionLine',
        to: '/faq?citycode=131237',
      },
      {
        title: '利用規約',
        icon: '$IconTermsLine',
        to: '/termofservice?citycode=131237',
      },
    ],
    facilityItems: [],
  },
  {
    city_name: 'hida',
    city_code: '212172',
    staffItems: [
      {
        title: 'お知らせ管理',
        icon: '$IconSettingNotificationLine',
        to: `/admin/notification?citycode=212172`,
      },
      {
        title: 'お問合せ管理',
        icon: '$IconSettingInquiryLine',
        to: `/admin/faq/list?citycode=212172`,
      },
      {
        title: 'ユーザー管理',
        icon: '$IconSettingUserLine',
        to: `/admin/account/list?citycode=212172`,
      },
      {
        title: 'アンケート管理',
        icon: '$IconSurveyLine',
        to: '/admin/survey?citycode=212172',
      },
    ],
    userItems: [
      {
        title: 'ホーム',
        icon: '$IconHomeLine',
        to: '/home?citycode=212172',
      },
      {
        title: 'お知らせ',
        icon: '$IconInformationLine',
        to: '/notification?citycode=212172',
      },
      {
        title: '障がい者支援情報',
        icon: '$IconBookletLine',
        to: '/booklet?citycode=212172',
      },
      {
        title: '各種相談窓口',
        icon: '$IconSupportLine',
        to: '/information?citycode=212172',
      },
      // {
      //   title: '障がい福祉情報',
      //   icon: '$IconServiceLine',
      //   to: 'https://www.city.hida.gifu.jp/site/sougouhukusi/',
      // },
      // {
      //   title: 'ミライロID',
      //   icon: '$IconIdLine',
      //   to: '/mirairo?citycode=212172',
      // },
      {
        title: 'よくある質問',
        icon: '$IconQuestionLine',
        to: '/faq?citycode=212172',
      },
      {
        title: '利用規約',
        icon: '$IconTermsLine',
        to: '/termofservice?citycode=212172',
      },
    ],
    facilityItems: [],
  },
  {
    city_name: 'nasushiobara',
    city_code: '092134',
    staffItems: [
      {
        title: 'お知らせ管理',
        icon: '$IconSettingNotificationLine',
        to: `/admin/notification?citycode=092134`,
      },
      {
        title: 'お問合せ管理',
        icon: '$IconSettingInquiryLine',
        to: `/admin/faq/list?citycode=092134`,
      },
      {
        title: 'ユーザー管理',
        icon: '$IconSettingUserLine',
        to: `/admin/account/list?citycode=092134`,
      },
      {
        title: 'アンケート管理',
        icon: '$IconSurveyLine',
        to: '/admin/survey?citycode=092134',
      },
      {
        title: '施設管理',
        icon: '$IconSettingOfficeLine',
        to: '/admin/facility?citycode=092134',
      },
    ],
    userItems: [
      {
        title: 'ホーム',
        icon: '$IconHomeLine',
        to: '/home?citycode=092134',
      },
      {
        title: 'お知らせ',
        icon: '$IconInformationLine',
        to: '/notification?citycode=092134',
      },
      {
        title: '事業所一覧',
        icon: '$IconFacilityLine',
        to: '/congestion?citycode=092134',
      },
      {
        title: 'るぴなすノート',
        icon: '$IconBookletLine',
        to: '/support-file/start?citycode=092134',
      },
      {
        title: '障害者支援情報',
        icon: '$IconServiceLine',
        to: '/booklet?citycode=092134',
      },
      {
        title: 'よくある質問',
        icon: '$IconQuestionLine',
        to: '/faq?citycode=092134',
      },
      {
        title: '利用規約',
        icon: '$IconTermsLine',
        to: '/termofservice?citycode=092134',
      },
    ],
    facilityItems: [],
  },
]