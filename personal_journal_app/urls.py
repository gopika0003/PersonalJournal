from django.urls import path
from . import views

urlpatterns = [
    path('new-entry/', views.new_entry, name='new_entry'),
    path('view/', views.view_page, name='view_entries'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Optional
]