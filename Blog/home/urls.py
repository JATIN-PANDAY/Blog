from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
     path('', views.index,name='index'),
     path("single_blog/<uid>",views.single_blog,name='single_blog'),
     path('contact',views.contact,name='contact'),
     path("comment/<uid>",views.comment,name="comment"),
     # path("popular_posts",views.popular_posts,name="popular_posts"),
     path("categories/<uid>",views.categories,name='categories'),
     path("search_posts",views.search_posts,name="search_posts"),
]
