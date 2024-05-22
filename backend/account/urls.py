from django.urls.conf import path

from account import views

urlpatterns = [
    path('token-obtain/', views.TokenObtainView.as_view()),
    path('token-refresh/', views.TokenRefreshView.as_view()),
    path('token-verify/', views.TokenVerifyView.as_view()),
    path('user/', views.UserView.as_view()),
    path('sign-up/', views.SignUpView.as_view()),
    path('sign-up-facility-user/', views.SignUpFacilityUserView.as_view()),
    path('activate/', views.ActivateAccount.as_view()),
    path('request-reset-password/', views.RequestResetPasswordView.as_view()),
    path('reset-password/', views.ResetPasswordView.as_view()),
    path('user-info/', views.UserInfoView.as_view()),
    path('user-info/<str:pk>/', views.UserInfoView.as_view()),
    path('help-card-pdf/', views.HelpCardView.as_view()),
    path('user-list/', views.UserListView.as_view()),
    path('user-list-csv/', views.UserListCsvView.as_view()),
    path('user-list/<str:pk>/', views.UserListView.as_view()),
    path('facility-user-list/', views.FacilityUserListView.as_view()),
]
