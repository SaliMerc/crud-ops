"""
URL configuration for Shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Admin import views

urlpatterns = [
    path('', views.admin, name='admin'),
    path('add_item/', views.add_item, name='add_item'),
    
    path('delete/<int:product_id>/', views.delete, name='delete'),
    path('update/<int:product_id>/', views.update_item, name='update'),
    
    path('mpesa-payment/', views.mpesa_payment, name='mpesa_payment'),
    path('payments-made/', views.payments_made, name='payments_made'),
    
]
