from django.urls import path, include

from BulletScreen import views

urlpatterns = [
    path('ws/s/', views.index, name='index'),
]












