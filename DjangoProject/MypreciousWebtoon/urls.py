"""MypreciousWebtoon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
import contentsApp.views

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path('admin/', admin.site.urls),
    path('account/', include('accountApp.urls')),
    path('accounts/', include('allauth.urls')),
    path('detail/<int:id>', contentsApp.views.webtoon_detail, name='datail'),
    path('all', contentsApp.views.list_test),
]

# media file serve
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
