"""
URL configuration for SocialNetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from social_network_app.views import login_request, register_request, logout_request
import social_network_app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_request),
    path('register/', register_request),
    path('logout/', logout_request),
    path('api/v1/', include('social_network_app.api.urls'))
]
