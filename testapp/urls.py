# from .views import RegisterAPI
from django.urls import path
from .views import *

from . import views
from django.contrib.auth import views as auth_views

from django.utils.translation import gettext as _

from django.urls import path,include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.index, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('download/', views.download, name='download'),
    path('video/', views.video, name='video'),
    path('faq/', views.faq, name='faq'),
    
    
    path('logout/', views.logoutUser, name='logout'),
    
    path('setfinder/', views.setfinder, name='setfinder'),
    path('upload_file/', views.upload_file, name='upload_file'),
    
    path('video_cards/', views.video_cards, name='video_cards'),
    path('CreateCheckoutSessionView/',views.CreateCheckoutSessionView,name='CreateCheckoutSessionView'),
    path('success/',views.success,name='success'),
    path('cancel/',views.cancel,name='cancel'),
    path('webhook/stripe',views.my_webhook_view,name='webhook-stripe'),
    
    path('download/',views.handle_custom_download_submit,name='handle_custom_download_submit'),
    
    


   
]