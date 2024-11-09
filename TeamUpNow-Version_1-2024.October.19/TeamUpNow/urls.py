"""TeamUpNow URL Configuration

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
from django.shortcuts import redirect

# Redirect from the root URL to /user/login/
def redirect_to_login(request):
    return redirect('/user/login/')

urlpatterns = [
    # Redirect the root URL to login
    path('', redirect_to_login),  # Root URL points to login

    # Other URL patterns
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('user/', include('authy.urls')),
    path('notifications/', include('notifications.urls')),
    path('<username>/', profile, name='profile'),
    path('<username>/saved', profile_saved, name='profilefavorites'),
    path('<username>/follow/<option>', mentoring_follow, name='follow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# from django.contrib import admin
# from django.urls import path, include
# from django.conf.urls.static import static
# from django.conf import settings

# from authy.views import profile, profile_saved, mentoring_follow

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('post/', include('post.urls')),
#     path('user/', include('authy.urls')),
#     path('notifications/', include('notifications.urls')),
#     path('<username>/', profile, name='profile'),
#     path('<username>/saved', profile, name='profilefavorites'),
#     path('<username>/follow/<option>', mentoring_follow, name='follow'),

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
