from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [    
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('register/', views.create_client, name='register'),
    
    path('login_user/', views.login_view, name='login_user'),
    path('logout_user/', views.logout_view, name='logout_user'),
    
    path('search_client/', views.search_client, name='search_client'),    
    path('create_service/<int:id_client>/', views.create_service, name='create_service'),
    
    
    path('services_view/', views.services_view, name='services_view'),
    
    path('generate_pdf/<int:id_service>/', views.generate_pdf, name='generate_pdf'),
    
    
    
    path('update_service/<int:id_service>/', views.update_service, name='update_service'),
    
    path('view_client_service/<int:id_service>/', views.view_client_service, name='view_client_service'),    
    
    
    path('search_car/', views.search_car, name='search_car'),    
    path('client_list/', views.client_list, name='client_list'),
    path('client_detail/<int:id_client>', views.client_detail, name='client_detail'),
    path('update_client/<int:id_client>', views.update_client, name='update_client'),
    path('update_car/<int:id_client>', views.update_car, name='update_car'),
    path('car_detail/<int:id_client>', views.car_detail, name='car_detail'),
] 

