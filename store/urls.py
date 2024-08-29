from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from haystack.views import SearchView

urlpatterns = [
    path('', views.store, name="store"),
    path('profile', views.profile, name="profile"),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('employee', views.employee, name='employee'),
    path('employee_panel', views.employee_panel, name='employee_panel'),
    path('add_good', views.add_good, name='add_good'),
    path('delete_good', views.delete_good, name='delete_good'),
    path('report', views.report, name='report'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('delete-cart-item/', views.delete_cart_item, name='delete_cart_item'),
    path('search/', SearchView(), name='haystack_search'),
    path('place_order', views.place_order, name='place_order')
]

