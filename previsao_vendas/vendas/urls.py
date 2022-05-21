from django.urls import path
from . import views


app_name = 'vendas'
urlpatterns = [
    path('', views.index, name='vendas_index'),
    path('create/', views.create, name='vendas_create'),
    path('store/', views.store, name='vendas_store'),
    path('edit/<int:id>', views.edit, name='vendas_edit'),
    path('update/<int:id>', views.update, name='vendas_update'),
    path('delete/<int:id>', views.delete, name='vendas_delete'),
    path('charts/', views.charts, name='vendas_charts'),
]
