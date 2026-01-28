"""
URL configuration for GameValut project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views # Importiamo le viste di login standard
from core.views import delete_thread, homepage, registration, create_thread, thread_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage', homepage, name='homepage'),
    re_path(r'^$', homepage, name='homepage'),  # La root va alla homepage
    # Registrazione personalizzata
    path('registration/', registration, name='registration'),

    # Login e Logout standard di Django
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),

    # Per l'aggiunta di thread
    path('newthread/', create_thread, name='create_thread'),
    path('thread/<int:pk>/', thread_detail, name='thread_detail'),
    path('thread/<int:pk>/delete/', delete_thread, name='delete_thread'),

    # Includiamo le URL dell'app "events"
    path('events/', include('events.urls')), 
]