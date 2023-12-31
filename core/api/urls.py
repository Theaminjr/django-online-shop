from django.urls import path
from core.api.views import CreateOtp,CheckOtp,ProfileView,AddressView,AddressListView,SignUpView,LogInView,ForgotPasswordLinkGeneratorView,PasswordChangeView,ChangePasswordUUIDView
urlpatterns = [
    path("askotp/",CreateOtp.as_view()),# create otp code for the phone number provided
    path("checkotp/",CheckOtp.as_view()),# if otp correct create/login user
    path("signup/",SignUpView.as_view()),# normal sign up 
    path("login/",LogInView.as_view()),# login using unique identifier and correlated password
    path("changepassword/<uuid:uuid>/",ChangePasswordUUIDView.as_view()),# change password using link generated by forgot password
    path("changepassword/",PasswordChangeView.as_view()),# change password if you are already logged in
    path("forgotpassword/",ForgotPasswordLinkGeneratorView.as_view()),# ask for change password link
    path("profile/",ProfileView.as_view()), # get user profile and update it
    path("address/<int:id>/",AddressView.as_view()),# delete a specific address
    path("addresses/",AddressListView.as_view()),# create new address or get all wxisiting ones
]
