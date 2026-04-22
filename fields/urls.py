from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-status/<int:pk>/', views.update_field_status, name='update_field_status'),
    path('edit-notes/<int:pk>/', views.edit_notes, name='edit_notes'),
    path('save-notes/<int:pk>/', views.save_notes, name='save_notes'),
    path('get-notes/<int:pk>/', views.save_notes, name='get_notes'), # Reuses save logic to just view
]