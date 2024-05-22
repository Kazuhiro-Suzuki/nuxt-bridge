from django.urls.conf import path

from app import views

urlpatterns = [
    # app
    path('region/', views.RegionView.as_view()),
    path('upload_file/', views.UploadFileView.as_view()),
    path('upload_file/public/', views.UploadFilePublicView.as_view()),
    path('information_file/', views.InformationFileView.as_view()),
    path('notification/', views.NotificationView.as_view()),
    path('notification/<int:pk>/', views.NotificationDetailView.as_view()),
    path('notification/public/', views.NotificationPublicView.as_view()),
    path('facility/', views.FacilityView.as_view()),
    path('facility/<int:pk>/', views.FacilityView.as_view()),
    path('facility_list/', views.FacilityListView.as_view()),
    path('facility_list/region_setting/', views.FacilityListRegionSetting.as_view()),    
    path('facility_list/file/', views.FacilityListFile.as_view()),    
    path('reservation_connection/', views.ReservationConnectionView.as_view()),
    path('facility/public/', views.FacilityPublicView.as_view()),
    path('facility/all_public/', views.FacilityAllPublicView.as_view()),
    path('faq/', views.FAQView.as_view()),
    path('faq/inquiry/', views.InquiryView.as_view()),
    path('faq/inquiry/<int:pk>', views.InquiryView.as_view()),
    path('faq/admin/inquiry/', views.InquiryAdminListView.as_view()),
    path('faq/admin/inquiry/<userId>', views.InquiryAdminDetailView.as_view()),
    path('firebase_token/', views.FirebaseTokenView.as_view()),
    path('firebase_verify_token/', views.FirebaseTokenVerifyView.as_view()),
    path('micro_service/', views.MicroServiceView.as_view()),
    path('support_file/', views.SupportFileView.as_view()),
    path('support_file/img/', views.SupportFileUploadFileView.as_view()),
    path('support_file/repl/', views.SupportFileReplView.as_view()),
    path('support_file/repl/id/', views.SupportFileReplIdView.as_view()),
    path('support_file/pdf/', views.SupportFilePDFView.as_view()),


    # city ca api
    path('reservation_slot/', views.ReservationSlotView.as_view()),
    path('reservation_slot_native/', views.ReservationSlotNativeView.as_view()),
    path('reservation_slot_customize/', views.ReservationSlotCustomizeView.as_view()),
    path('reservation_facility/', views.ReservationFacilityView.as_view()),
    path('reservation_facility/detail/', views.ReservationFacilityDetailView.as_view()),
    path('reservation_temporary/', views.ReservationTemporaryView.as_view()),
    path('reservation_temporary/<str:pk>/', views.ReservationTemporaryView.as_view()),
    path('reservation/', views.ReservationView.as_view()),
    path('reservation/<str:pk>/', views.ReservationView.as_view()),

    # Mirairo
    path('mirairo/initial/', views.MirairoConnectInitialDataView.as_view()),
    path('mirairo/connect/', views.MirairoConnectView.as_view()),
    path('mirairo/disconnect/', views.MirairoDisconnectView.as_view()),
]
