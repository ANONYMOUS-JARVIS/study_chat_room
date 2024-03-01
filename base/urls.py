from django.urls import path
from . import views
from django.contrib.auth.models import User

urlpatterns = [
   path('',views.home,name="home"),
   path('room/<str:pk>/',views.room,name="room"),
   path('creat-form/',views.creat_form,name="creat-form"),
   path('update-form/<str:pk>/',views.update_room,name="upate-form"),
   path('delete-form/<str:pk>/',views.delete_room,name="delete-form"),
   path('user_pro/<str:pk>/',views.user_profile,name="user_pro"),
   path('login/',views.login_form,name="login"),
   path('Register/',views.register_page,name="Register"),
   path('logout/',views.logout_page,name="logout"),
   path('delete-message/<str:pk>/',views.delete_message,name="delete-message"),
   path('update-user/',views.updateUser,name="update-user"),
   path('topicList/',views.topicList,name="topicList"),
   path('activity/',views.activity,name="activity"),

]