from django.contrib import admin
from django.urls import path, include, reverse
from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('tasks/', include('tasks.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('', RedirectView.as_view(url='login/')),
]
