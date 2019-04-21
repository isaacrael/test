"""cdh_ecosystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path, re_path
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

# Admin page
path('admin/', admin.site.urls),
# About page
path('', include('cdh_ecosystem_quiz.urls'), name='index'),
# Account page include registration.backends.default.urls
path('account/', include('registration.backends.default.urls')),
# Registration page
path('account/register/', include('registration.backends.default.urls')),
# Login page
path('account/login/', include('registration.backends.default.urls')),
# Quiz url
re_path(r'^quiz/', include('cdh_ecosystem_quiz.urls', namespace='cdh_ecosystem_quiz')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
