from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Produtos
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('<int:pk>/toggle-status/', views.product_toggle_status, name='product_toggle_status'),
    
    # Categorias
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('categories/<int:pk>/toggle-status/', views.category_toggle_status, name='category_toggle_status'),

    # Escalas
    path('scales/', views.scale_list, name='scale_list'),
    path('scales/create/', views.scale_create, name='scale_create'),
    path('scales/<int:pk>/edit/', views.scale_edit, name='scale_edit'),
    path('scales/<int:pk>/delete/', views.scale_delete, name='scale_delete'),
    path('scales/<int:pk>/toggle-status/', views.scale_toggle_status, name='scale_toggle_status'),

    # Tipos de Produto
    path('product-types/', views.product_type_list, name='product_type_list'),
    path('product-types/create/', views.product_type_create, name='product_type_create'),
    path('product-types/<int:pk>/edit/', views.product_type_edit, name='product_type_edit'),
    path('product-types/<int:pk>/toggle-status/', views.product_type_toggle_status, name='product_type_toggle_status'),

    # Países
    path('countries/', views.country_list, name='country_list'),
    path('countries/<int:pk>/edit/', views.country_edit, name='country_edit'),
    path('countries/<int:pk>/toggle-status/', views.country_toggle_status, name='country_toggle_status'),

    # AJAX endpoints
    path('product-type/create/ajax/', views.product_type_create_ajax, name='product_type_create_ajax'),
    path('category/create/ajax/', views.category_create_ajax, name='category_create_ajax'),
    path('scale/create/ajax/', views.scale_create_ajax, name='scale_create_ajax'),
]