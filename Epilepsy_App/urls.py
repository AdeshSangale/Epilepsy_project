from django.urls import path,include

from . import views

urlpatterns = [
    
    path('',views.index),
    path('register/', views.register, name='register'),
    path('login_view/', views.login_view, name='login_view'),
    path('predict', views.predict, name='predict'),
    path('result', views.result, name='result'),
    path('Precautions/',views.Precautions,name='Precautions'),
    path('about/',views.about,name='about'),
    path('display_csv/',views.display_csv, name='display_csv'),

]