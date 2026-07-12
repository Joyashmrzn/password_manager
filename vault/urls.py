from django.urls import path
from . import views

urlpatterns = [
    path('', views.vault_list, name='vault_list'),
    path('add/', views.vault_add, name='vault_add'),
    path('<int:pk>/', views.vault_view_password, name='vault_view_password'),
    path('<int:pk>/delete/', views.vault_delete, name='vault_delete'),
]