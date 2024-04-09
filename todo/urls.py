from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from tasks.views import TaskLoginView, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('tasks/', include('tasks.urls')),
    path('login/', TaskLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', RedirectView.as_view(url='login/')),
    path('register/', register, name="register"),
]
