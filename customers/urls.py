from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # Listagem e busca
    path('', views.customer_list, name='customer_list'),
    path('search/', views.customer_search, name='customer_search'),
    
    # CRUD básico
    path('create/', views.customer_create, name='customer_create'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    # Ações adicionais
    path('<int:pk>/toggle-status/', views.customer_toggle_status, name='customer_toggle_status'),
]