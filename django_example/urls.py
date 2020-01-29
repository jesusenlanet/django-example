"""django_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from usermanage import views as usermanage_views
from usermanage.views import IbanUserList, IbanUserDetail, IbanUserDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls', namespace='social')),
    path('', usermanage_views.index),
    path('logout/', usermanage_views.logout_view, name='logout'),
    path('v1/api/users/', IbanUserList.as_view(), name='user-list'),
    path('v1/api/users/<int:pk>/', IbanUserDetail.as_view(), name='user-detail'),
    path('v1/api/users/<int:pk>/delete/', IbanUserDelete.as_view(), name='user-delete'),
]
