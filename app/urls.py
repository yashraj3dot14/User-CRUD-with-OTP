from django.urls import path
from . import views

app_name = 'user_reg_app'
urlpatterns = [
    path('signup/',views.signup, name= 'signup'),
    path('signin/', views.signin, name= 'signin'),
    path('generate_otp/', views.otp_generate, name= 'generate_otp'),
    path('verify_otp/', views.otp_login, name= 'otp_login'),
]