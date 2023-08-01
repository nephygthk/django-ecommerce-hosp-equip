from django.urls import path, include

from . import views

app_name = 'orders'
urlpatterns = [
    path('edit_order/<slug>/', views.EditOrderView.as_view(), name='edit_order'),
    path('delete_order/<slug>/', views.delete_order, name='delete_order'),
    path('view_receipt/<slug>/', views.view_receipt, name='view_receipt'),
]