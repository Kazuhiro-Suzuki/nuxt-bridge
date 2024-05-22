import Vue from 'vue'

// atoms buttons
import LinkButton from '~/components/atoms/buttons/LinkButton.vue'
import NormalButton from '~/components/atoms/buttons/NormalButton.vue'
import NormalMiniButton from '~/components/atoms/buttons/NormalMiniButton'
import OutlinedButton from '~/components/atoms/buttons/OutlinedButton.vue'
import TextButton from '~/components/atoms/buttons/TextButton.vue'

// atoms images
import LogoImage from '~/components/atoms/images/LogoImage.vue'

// atoms inputs
import TextField from '~/components/atoms/inputs/TextField.vue'
import TextArea from '~/components/atoms/inputs/TextArea.vue'
import CheckBox from '~/components/atoms/inputs/CheckBox'
import RadioButton from '~/components/atoms/inputs/RadioButton'
import SelectBox from '~/components/atoms/inputs/SelectBox'

// atoms titles
import DenseToolBar from '~/components/atoms/titles/DenseToolBar.vue'

// molecules
import ErrorAlert from '~/components/molecules/ErrorAlert.vue'
import CompleteSnackbar from '~/components/molecules/CompleteSnackbar.vue'
import Confirmation from '~/components/molecules/Confirmation.vue'
import LoginCard from '~/components/molecules/LoginCard.vue'
import LoginCardOneRow from '~/components/molecules/LoginCardOneRow.vue'
import MainMenuButton from '~/components/molecules/MainMenuButton.vue'
import HomeMainMenuButton from '~/components/molecules/HomeMainMenuButton.vue'
import NotificationCard from '~/components/molecules/NotificationCard.vue'
import NotificationSimpleCard from '~/components/molecules/NotificationSimpleCard.vue'
import NotificationSimpleText from '~/components/molecules/NotificationSimpleText.vue'
import NotificationList from '~/components/molecules/NotificationList.vue'
import SearchField from '~/components/molecules/SearchField.vue'
import TermOfServiceText from '~/components/molecules/TermOfServiceText.vue'
import ReservationFacilityInfo2 from '~/components/molecules/ReservationFacilityInfo2'


// organisms account
import LoginForm from '~/components/organisms/account/LoginForm.vue'
// import SignUpForm from '~/components/organisms/account/SignUpForm.vue'
// import ProfileCard from '~/components/organisms/account/ProfileCard.vue'
import FacilityUserProfileCard from '~/components/organisms/account/facility/FacilityUserProfileCard.vue'
import NewFacilityUserPost from '~/components/organisms/account/facility/NewFacilityUserPost.vue'
import FacilityUserTable from '~/components/organisms/account/facility/FacilityUserTable.vue'
import ConfirmFacilityUser from '~/components/organisms/account/facility/ConfirmFacilityUser.vue'
import UserListTable from '~/components/organisms/account/UserListTable.vue'
import ConfirmEmailForm from '~/components/organisms/account/ConfirmEmailForm.vue'
import ResetPasswordForm from '~/components/organisms/account/ResetPasswordForm.vue'
import AccountDeleteCard from '~/components/organisms/account/AccountDeleteCard.vue'

// organisms facility
import ConfirmFacility from '~/components/organisms/facility/ConfirmFacility.vue'
import NewFacilityPost from '~/components/organisms/facility/NewFacilityPost.vue'
import FacilityTable from '~/components/organisms/facility/FacilityTable.vue'
import DisabledFacilityList from '~/components/organisms/facility/DisabledFacilityList'
import DisabledFacilityDetail from '~/components/organisms/facility/DisabledFacilityDetail'

// organisms faq
import ContactInfoCard from '~/components/organisms/faq/ContactInfoCard.vue'
import NewInquiryPost from '~/components/organisms/faq/NewInquiryPost.vue'
import InquiryList from '~/components/organisms/faq/InquiryList.vue'
import AdminInquiryList from '~/components/organisms/faq/AdminInquiryList.vue'
import FaqCard from '~/components/organisms/faq/FaqCard.vue'
import FaqHome from '~/components/organisms/faq/FaqHome.vue'

// organisms history
import HistoryCard from '~/components/organisms/history/HistoryCard'

// organisms information
// import ChigasakiInfoCard from '~/components/organisms/information/chigasaki/ChigasakiInfoCard'
// import MinatoInfoCard from '~/components/organisms/information/minato/MinatoInfoCard'




// organisms mirairo
import MirairoConnectCard from '~/components/organisms/mirairo/MirairoConnectCard.vue'
import MirairoClosedCard from '~/components/organisms/mirairo/MirairoClosedCard.vue'
import MirairoIntroCard from '~/components/organisms/mirairo/MirairoIntroCard.vue'
import MirairoTitle from '~/components/organisms/mirairo/MirairoTitle.vue'
import MirairoInfoCard from '~/components/organisms/mirairo/MirairoInfoCard.vue'

// organisms notification
import NewNoticePost from '~/components/organisms/notification/NewNoticePost.vue'
import NotificationTable from '~/components/organisms/notification/NotificationTable.vue'
import ConfirmCard from '~/components/organisms/notification/ConfirmCard.vue'

// organisms reservation
import AnswerForm from '~/components/organisms/reservation/AnswerForm'
import SlotCard from '~/components/organisms/reservation/SlotCard'
import ReservationConfirmCard from '~/components/organisms/reservation/ReservationConfirmCard'
import ReservationCompleteCard from '~/components/organisms/reservation/ReservationCompleteCard'
import FacilityList from '~/components/organisms/reservation/FacilityList.vue'
import FacilityDetailCard from '~/components/organisms/reservation/FacilityDetailCard'
import ReservationCard from '~/components/organisms/reservation/ReservationCard.vue'
import ReservationHome from '~/components/organisms/reservation/ReservationHome.vue'

Vue.mixin(
  {
    components: {
      // atoms
      LinkButton,
      NormalButton,
      NormalMiniButton,
      OutlinedButton,
      TextButton,
      LogoImage,
      DenseToolBar,
      CheckBox,
      RadioButton,
      SelectBox,
      // molecules
      ErrorAlert,
      CompleteSnackbar,
      Confirmation,
      LoginCard,
      LoginCardOneRow,
      TextField,
      TextArea,
      MainMenuButton,
      HomeMainMenuButton,
      NotificationCard,
      NotificationSimpleCard,
      NotificationSimpleText,
      NotificationList,
      SearchField,
      ReservationFacilityInfo2,
      // organisms
      MirairoConnectCard,
      MirairoClosedCard,
      MirairoIntroCard,
      MirairoInfoCard,
      MirairoTitle,
      ConfirmCard,
      ConfirmFacility,
      ConfirmEmailForm,
      LoginForm,
      NewNoticePost,
      NotificationTable,
      NewFacilityPost,
      NewFacilityUserPost,
      ConfirmFacilityUser,
      FacilityTable,
      FacilityUserTable,
      FacilityUserProfileCard,
      FacilityList,
      ResetPasswordForm,
      AccountDeleteCard,
      // SignUpForm
      // ProfileCard,
      UserListTable,
      FacilityDetailCard,
      AnswerForm,
      ContactInfoCard,
      NewInquiryPost,
      InquiryList,
      AdminInquiryList,
      FaqCard,
      FaqHome,
      ReservationCard,
      ReservationHome,
      HistoryCard,
      // ChigasakiInfoCard,
      // MinatoInfoCard,
      SlotCard,
      ReservationConfirmCard,
      TermOfServiceText,
      ReservationCompleteCard,
      DisabledFacilityList,
      DisabledFacilityDetail,
    }
  }
)
