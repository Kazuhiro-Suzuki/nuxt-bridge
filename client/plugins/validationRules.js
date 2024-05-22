import moment from 'moment'

export default function rules({}, inject) {
  inject('rules', validationRules)
}

export function isEmpty(value, trim = false) {
  return (
    value === null ||
    value === undefined ||
    (trim ? value.trim() : value) === ''
  )
}

function str(value) {
  return '' + value
}

export function validateDate(year, month, day) {
    if (!moment(`${year}-${month}-${day}`).isValid()) {
      return '存在しない日付です。'
    }
    return true
}

// これは全角スペース→ \u3000
const jaFullPattern = /^[ぁ-んァ-ヶー一-龠々０-９Ａ-Ｚａ-ｚ－・ \u3000]*$/
// eslint-disable-next-line no-control-regex
const jaFullTextareaPattern = /^[^\x01-\x09\x0B-\x0C\x0E-\x7E\uFF61-\uFF9F]*$/
const jaFullKanaPattern = /^[ヴア-ン゛゜ァ-ォャ-ョー－「」、 \u3000]*$/
const jaHalfKanaPattern = /^[ｦ-ﾟ ]*$/
const jaKanaPattern = /^[ア-ン゛゜ァ-ォャ-ョー－「」、\u3000ｦ-ﾟ ]*$/
const halfNumPattern = /^[0-9]*$/
const hexNumPattern = /^[0-9A-F]*$/
const halfAlphaNumPattern = /^[a-zA-Z0-9]*$/
const phoneNumberPattern = /^[0-9]*$/
const alphaNumChars =
  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
const decimalPattern = /^[0-9]+(\.[0-9]+)?$/

export const validationRules = {
  required: (value) => !isEmpty(value) || '必須項目です',
  checkRequired: (msg) => (value) => value || msg,
  selectRequired: (value) => !isEmpty(value) || '選択してください',
  selectArrayRequired: (value) => value.length > 0 || '選択してください',
  requiredWithMessage: (message) => (value) => !isEmpty(value) || message,
  minLength: (length) => (value) =>
    isEmpty(value) ||
    str(value).length >= length ||
    `最低${length}文字で入力してください`,
  maxLength: (length, message = `最大${length}文字で入力してください`) => (
    value
  ) => isEmpty(value) || str(value).length <= length || message,
  minNum: (num) => (value) =>
    isEmpty(value) ||
    Number(value) >= num ||
    `${num}以上の数値を入力してください`,
  maxNum: (num) => (value) =>
    isEmpty(value) ||
    Number(value) <= num ||
    `${num}以下の数値を入力してください`,
  minInteger: (num) => (value) =>
    isEmpty(value) ||
    (halfNumPattern.test(str(value)) && Number(value) >= num) ||
    `${num}以上の整数を入力してください`,
  maxInteger: (num) => (value) =>
    isEmpty(value) ||
    (halfNumPattern.test(str(value)) && Number(value) <= num) ||
    `${num}以下の整数を入力してください`,
  integerBetween: (min, max) => (value) =>
    isEmpty(value) ||
    (halfNumPattern.test(str(value)) &&
      Number(value) >= min &&
      Number(value) <= max) ||
    `${min}以上${max}以下の整数を入力してください`,
  jaFull: (value) =>
    isEmpty(value) ||
    jaFullPattern.test(str(value)) ||
    '全角文字で入力してください',
  jaFullTextarea: (value) =>
    isEmpty(value) ||
    jaFullTextareaPattern.test(str(value)) ||
    '全角文字で入力してください',
  jaFullKana: (value) =>
    isEmpty(value) ||
    jaFullKanaPattern.test(str(value)) ||
    '全角カタカナで入力してください',
  jaHalfKana: (value) =>
    isEmpty(value) ||
    jaHalfKanaPattern.test(str(value)) ||
    '半角カタカナで入力してください',
  jaKana: (value) =>
    isEmpty(value) ||
    jaKanaPattern.test(str(value)) ||
    '全角カタカナまたは半角カタカナで入力してください',
  halfNum: (value) =>
    isEmpty(value) ||
    halfNumPattern.test(str(value)) ||
    '半角数字で入力してください',
  hexNumWithLengthExact: (length) => (value) =>
    isEmpty(value) ||
    (hexNumPattern.test(str(value)) && str(value).length === length) ||
    `${length}文字の16進数文字列(0-9, A-F)で入力してください`,
  halfAlphaNum: (value) =>
    isEmpty(value) ||
    halfAlphaNumPattern.test(str(value)) ||
    '半角英数で入力してください',
  halfAlphaNumWith: (additionalChars) => (value) => {
    const acceptedChars = alphaNumChars + additionalChars
    return (
      isEmpty(value) ||
      str(value)
        .split('')
        .every((c) => acceptedChars.includes(c)) ||
      `半角英数および「${additionalChars}」で入力してください`
    )
  },
  halfNumWithLengthExact: (length) => (value) =>
    isEmpty(value) ||
    (halfNumPattern.test(str(value)) && str(value).length === length) ||
    `${length}文字の半角数字で入力してください`,
  halfNumWithMaxLength: (length) => (value) =>
    isEmpty(value) ||
    (halfNumPattern.test(str(value)) && str(value).length <= length) ||
    `${length}文字以下の半角数字で入力してください`,
  halfNumWithLengthBetween: (minLength, maxLength) => (value) =>
    isEmpty(value) ||
    (halfNumPattern.test(str(value)) &&
      str(value).length >= minLength &&
      str(value).length <= maxLength) ||
    `${minLength}文字以上${maxLength}文字以下の半角数字で入力してください`,
  phoneNumberIsLong: (value) => str(value).length <= 11 || '桁数が多すぎます',
  phoneNumberIsShort: (value) =>
    str(value).length >= 11 || '桁数が少なすぎます',
  isNumber: (value) =>
    isEmpty(value) ||
    phoneNumberPattern.test(str(value)) ||
    '半角数字で入力してください',
  onOrBeforeToday: (value) =>
    moment().diff(moment(value)) > 0 || '未来の日付は登録できません。',
  decimal: (value) =>
    isEmpty(value) ||
    decimalPattern.test(str(value)) ||
    '整数または小数で入力してください'
}
