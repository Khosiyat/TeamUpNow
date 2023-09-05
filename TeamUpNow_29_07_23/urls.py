"""TeamUpNow_29_07_23 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from authy.views import UserProfile, profilefavorites, follow

from TeamUpNow_29_07_23.views import teamUpNowTech_login, teamUpNowTech

from django.views.generic.base import RedirectView


urlpatterns = [
    # path('teamUpNowTech_login/', teamUpNowTech_login, name="teamUpNowTech_login"),

    # url(r'^(?P<path>.*)', teamupnow_redirect),

    # path('', RedirectView.as_view(url='https://www.teamupnow.tech/?q=%(term)s')),

    path(
        " ",
        RedirectView.as_view(url="teamupnow.tech/"),
    ),
    
    # path('/search/<term>/', RedirectView.as_view(url='https://www.teamupnow.tech/?q=%(term)s')),

    path('teamUpNowTech/', teamUpNowTech, name="teamUpNowTech"),

    path('', teamUpNowTech, name="teamUpNowTech"),



    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('post_StartUp/', include('post_StartUp.urls')),
    path('user/', include('authy.urls')),
    path('stories/', include('stories.urls')),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/saved', profilefavorites, name='profilefavorites'),
    path('<username>/follow/<option>', follow, name='follow'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
