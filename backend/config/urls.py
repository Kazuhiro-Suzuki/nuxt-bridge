"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls.conf import include

from app.views.common_view import health_check
from rest_framework_swagger.views import get_swagger_view
from app import views

schema_view = get_swagger_view(title='API Lists')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view),
    path('api/health-check/', health_check),
    path('api/v1/app/', include('app.urls')),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/account/', include('account.urls')),
    path('htp-api/form_output/', views.SupportFileFormOutputView.as_view()),
    path('htp-api/form_output/img/', views.SupportFileFormOutputFileView.as_view()),
]
