from django.contrib import admin
from django.urls import path
from User import views


urlpatterns = [
     path('signup', views.signup,name='signup'),
     # path('accounts/', include('allauth.urls')),
     path('signin',views.signin,name='signin'),
     path("logout",views.logout,name="logout"),
     path("postblog",views.postblog,name="postblog"),
     path("check",views.check,name='check'),
]
