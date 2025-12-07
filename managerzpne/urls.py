from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', csrf_exempt(auth_views.LogoutView.as_view()), name='logout'),
    path('logout/', csrf_exempt(auth_views.LogoutView.as_view()), name='logout'),
    path('', include('team.urls')),
]
