from django.urls import path
from . import views

urlpatterns = [
    path('assign-agent/<int:pk>/', views.assign_agent, name='assign_agent'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-status/<int:pk>/', views.update_field_status, name='update_field_status'),
    path('edit-notes/<int:pk>/', views.edit_notes, name='edit_notes'),
    path('save-notes/<int:pk>/', views.save_notes, name='save_notes'),
    path('get-notes/<int:pk>/', views.save_notes, name='get_notes'), # Reuses save logic to just view
    path('add-field/', views.add_field, name='add_field'),
    path('save-field/', views.save_new_field, name='save_new_field'),
    path('add-agent/', views.add_agent, name='add_agent'),
    path('save-agent/', views.save_new_agent, name='save_new_agent'),
]