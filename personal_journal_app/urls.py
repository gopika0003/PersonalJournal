from django.urls import path
from . import views

urlpatterns = [
    path('new-entry/', views.new_entry, name='new_entry'),
    path('view/', views.view_page, name='view_entries'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Optional
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('favorite/<int:entry_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('edit/<int:entry_id>/', views.view_page, name='edit_entry'),
    path('entry/<int:entry_id>/', views.read_entry, name='entry_detail'),
    path('favorites/', views.favorite_entries, name='favorite_entries'), 
]