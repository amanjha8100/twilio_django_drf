from django.urls import path
from .import views

urlpatterns = [
    path('room/',views.room,name="room"),
    path('room/access/<str:room>/', views.token,name="token")
]