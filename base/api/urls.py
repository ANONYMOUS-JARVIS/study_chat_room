from django.urls import path
from . import views

urlpatterns = [
       path('room/',views.getrooms),
       path('room/<str:pk>/',views.getroom_by_id),

]