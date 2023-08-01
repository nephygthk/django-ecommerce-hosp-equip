from django.urls import path
from django.contrib.auth import views as auth_views


from .import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('user_index_login/', views.user_index_login, name='user_index_login'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('admin_dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('customer_dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('add_product/', views.AddProductView.as_view(), name='add_product'),
    path('delete_customer/<pk>/', views.delete_customer, name='delete_customer'),
    path('delete_product/<pk>/', views.delete_product, name='delete_product'),
    path("logout/", auth_views.LogoutView.as_view(next_page="/account/login/"), name="logout"),
]