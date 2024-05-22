export default function ({ $axios, $config }, inject) {
  const api = new API($axios, $config)
  inject('api', api)
}

class API {
  constructor (axios, config) {
    this.axios = axios
    this.config = config
  }
  /*
    アカウント関連のAPI
  */
  async postSignUpInfo(payload) {
    const url = '/api/v1/account/sign-up/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async postSignUpFacilityUserInfo(payload) {
    const url = '/api/v1/account/sign-up-facility-user/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async postActivateAccount(payload) {
    const url = '/api/v1/account/activate/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async postRequestResetPassword(payload) {
    const url = '/api/v1/account/request-reset-password/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async postResetPassword(payload) {
    const url = '/api/v1/account/reset-password/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async getUserInfo() {
    let url = '/api/v1/account/user-info/'
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async getUserList(param) {
    let url = '/api/v1/account/user-list/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async getUserListCsv(param) {
    let url = '/api/v1/account/user-list-csv/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async putUserInfo(item) {
    let url = `/api/v1/account/user-info/${item.uid}/`
    // let payload = {
    //   'email': item.email,
    //   'phone_number': item.phone_number,
    //   'fax_number': item.fax_number,
    //   'is_subscribe': item.is_subscribe,
    // }
    try {
      return await this.axios.put(url, item)
    } catch (err) {
      return err.response
    }
  }
  async deleteUserInfo(item) {
    let url = `/api/v1/account/user-info/${item.uid}/`
    try {
      return await this.axios.delete(url)
    } catch (err) {
      return err.response
    }
  }
  async changeUserStatus(item) {
    let url = `/api/v1/account/user-list/${item.uid}/`
    let payload = {
      'is_active': item.is_active,
      'is_subscribe': item.is_subscribe,
      'is_dangerous': item.is_dangerous
    }
    try {
      return await this.axios.put(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async getFacilityUserList(param) {
    let url = '/api/v1/account/facility-user-list/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async getHelpCardPDF(param) {
    let url = '/api/v1/account/help-card-pdf/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async createHelpCardPDF() {
    let url = '/api/v1/account/help-card-pdf/'
    try {
      return await this.axios.post(url)
    } catch (err) {
      return err.response
    }
  }

  /*
    Region API
    自治体情報関連のAPI
  */
  async getRegion(param) {
    let url = '/api/v1/app/region/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }

  /*
    Notification API
    お知らせ関連のAPI
  */
  async getPublicNotification(param) {
    let url = '/api/v1/app/notification/public/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async getNotification(param) {
    let url = '/api/v1/app/notification/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async postNotification(payload) {
    const url = '/api/v1/app/notification/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async getNotificationDetail(id) {
    const url = `/api/v1/app/notification/${id}/`
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async putNotification(item) {
    const url = `/api/v1/app/notification/${item.id}/`
    const payload = {
      id: item.id,
      subject: item.subject,
      body: item.body,
      file_ids: item.file_ids,
      is_disaster_info: item.is_disaster_info,
      active_since: item.active_since,
      segment_birthday:item.segment_birthday,
      segment_birthday_year:item.segment_birthday_year,
      segment_birthday_month:item.segment_birthday_month,
      segment_address_block: item.segment_address_block,
      segment_age_range: item.segment_age_range,
      segment_user_type: item.segment_user_type,
      segment_disability_type:item.segment_disability_type,
      segment_notification_tag:item.segment_notification_tag,
      segment_notification_category:item.segment_notification_category,
    }
    try {
      return await this.axios.put(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async deleteNotification(id) {
    const url = `/api/v1/app/notification/${id}/`
    try {
      return await this.axios.delete(url)
    } catch (err) {
      return err.response
    }
  }

  /*
    UploadFile API
    ファイル関連のAPI
  */  
  async uploadAssets(payload, headers) {
    const url = '/api/v1/app/upload_file/'
    try {
      return await this.axios.post(url, payload, headers)

    } catch (err) {
      return err.response
    }
  }
  async deleteAssets(payload) {
    const param = {
      data: payload,
      headers: {
        'content-type': 'multipart/form-data'
      },
    }
    const url = '/api/v1/app/upload_file/'
    try {
      return await this.axios.delete(url, param)
    } catch (err) {
      return err.response
    }
  }

  /*
    Facility API　※使用しない
  */
  async getPublicFacilities(param) {
    let url = '/api/v1/app/facility/public/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async getAllPublicFacilities(param) {
    let url = '/api/v1/app/facility/all_public/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async postFacility(payload) {
    const url = '/api/v1/app/facility/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async putFacility(item) {
    const url = `/api/v1/app/facility/${item.id}/`
    const payload = {
      id: item.id,
      name: item.name,
      city_code: item.city_code
    }
    try {
      return await this.axios.put(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async deleteFacility(id) {
    const url = `/api/v1/app/facility/${id}/`
    try {
      return await this.axios.delete(url)
    } catch (err) {
      return err.response
    }
  }

  /*
    Slot API
    予約枠関連のAPI
  */
  async getSlot(param) {
    let url = '/api/v1/app/reservation_slot/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async postSlot(payload) {
    let url = '/api/v1/app/reservation_slot/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async postCustomizeSlot(payload) {
    let url = '/api/v1/app/reservation_slot_customize/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }

  /*
    Reservation Facility API
    施設関連のAPI
  */
  async getReservationFacility(param) {
    let url = '/api/v1/app/reservation_facility/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async getReservationFacilityDetail(param) {
    let url = '/api/v1/app/reservation_facility/detail/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async findReservationFacility(param, payload) {
    let url = '/api/v1/app/reservation_facility/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async getReservationConnection(param) {
    let url = '/api/v1/app/reservation_connection/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }

  /*
    Reservation Temporary API
    仮予約関連のAPI
  */
  async postReservationTmp(payload) {
    // 仮予約を実行
    let url = '/api/v1/app/reservation_temporary/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async cancelReservationTmp(param, payload) {
    // 仮予約をキャンセル
    let url = '/api/v1/app/reservation_temporary/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.put(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async getReservationTmp(param) {
    // 仮予約情報を取得
    let url = '/api/v1/app/reservation_temporary/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }

  /*
    Reservation API
    予約情報関連のAPI
  */
  async getReservation(param) {
    let url = '/api/v1/app/reservation/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async postReservation(payload) {
    let url = '/api/v1/app/reservation/'
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async cancelReservation(reservationId, payload) {
    // 仮予約をキャンセル
    const url = `/api/v1/app/reservation/${reservationId}/`
    try {
      return await this.axios.put(url, payload)
    } catch (err) {
      return err.response
    }
  }

  /*
    MirairoConnect API
    ミライロID連携関連のAPI
   */
  async getMirairoConnectInitialData(city_code) {
    let url = '/api/v1/app/mirairo/initial/'
    try {
      return await this.axios.get(url, { params: { city_code } })
    } catch (err) {
      return err.response
    }
  }

  /*
    FAQ API
  */
  async getFAQ(city_code) {
    let url = `/api/v1/app/faq/?city_code=${city_code}`
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  /*
    Inquiry API
  */
  async getUserInquiryList(param) {
    let url = '/api/v1/app/faq/inquiry/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async postNewInquiry(payload, param) {
    let url = '/api/v1/app/faq/inquiry/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async getAdminInquiryList(param) {
    let url = '/api/v1/app/faq/admin/inquiry/'
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async getAdminInquiryDetail(userId, param) {
    let url = `/api/v1/app/faq/admin/inquiry/${userId}`
    if (param) { url += '?' + param }
    try {
      return await this.axios.get(url)
    } catch (err) {
      return err.response
    }
  }
  async postNewReply(payload, param, userId) {
    let url = `/api/v1/app/faq/admin/inquiry/${userId}`
    if (param) { url += '?' + param }
    try {
      return await this.axios.post(url, payload)
    } catch (err) {
      return err.response
    }
  }
  async updateInquiryStatus(payload, param, userId) {
    let url = `/api/v1/app/faq/admin/inquiry/${userId}`
    if (param) { url += '?' + param }
    try {
      console.log(url, payload);
      return await this.axios.put(url, payload)
    } catch (err) {
      return err.response
    }
  }

  /*
    MicroService API
    マイクロサービス関連ののAPI
  */
    async getMicroServiceUrls(param) {
      let url = '/api/v1/app/micro_service/'
      if (param) { url += '?' + param }
      try {
        return await this.axios.get(url)
      } catch (err) {
        return err.response
      }
    }
}
