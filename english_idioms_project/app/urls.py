from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('random/', views.random_idiom_view, name='random_idiom'),
    path('quiz/', views.quiz_view, name='quiz'),
]
