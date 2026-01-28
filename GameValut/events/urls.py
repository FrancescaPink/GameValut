from django.urls import path
from .views import create_event, delete_event, event_detail, event_list, update_event

urlpatterns = [
    path('', event_list, name='event_list'),
    path('new/', create_event, name='create_event'),
    path('<int:pk>/', event_detail, name='event_detail'),
    path('<int:pk>/delete/', delete_event, name='delete_event'),
    path('<int:pk>/edit/', update_event, name='update_event'),
]