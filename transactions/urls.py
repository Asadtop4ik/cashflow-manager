from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('category/filter_by_type/', views.filter_categories_by_type, name='filter_categories_by_type'),
    path('subcategory/filter_by_category/', views.filter_subcategories_by_category, name='filter_subcategories_by_category'),
]