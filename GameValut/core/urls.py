from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views         
from core.views import delete_thread, homepage, registration, create_thread, thread_detail, announcement_list, create_announcement, announcement_detail, edit_announcement, delete_announcement
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('homepage', homepage, name='homepage'),
    re_path(r'^$', homepage, name='homepage'),          # Grazie a questo la root va alla homepage
    # Registrazione personalizzata
    path('registration/', registration, name='registration'),
    # Login e Logout standard di Django
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
    # Per l'aggiunta di thread
    path('newthread/', create_thread, name='create_thread'),
    path('thread/<int:pk>/', thread_detail, name='thread_detail'),
    path('thread/<int:pk>/delete/', delete_thread, name='delete_thread'),
    path('thread/<int:pk>/follow/', views.toggle_follow_thread, name='toggle_follow_thread'),
    # Per la gestione degli annunci
    path('news/', views.announcement_list, name='announcement_list'),
    path('news/create/', views.create_announcement, name='create_announcement'), # <--- QUESTA MANCAVA
    path('news/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('news/<int:pk>/edit/', views.edit_announcement, name='edit_announcement'),
    path('news/<int:pk>/delete/', views.delete_announcement, name='delete_announcement'),
]