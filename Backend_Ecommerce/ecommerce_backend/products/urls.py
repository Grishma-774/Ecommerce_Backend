
from django.urls import path
from .views import product_list,product,AdminProductListCreate, AdminProductDetail

urlpatterns = [
    path('', product_list),
    path('<int:pk>/',product),
    path("admin/products/", AdminProductListCreate.as_view()),
    path("admin/products/<int:pk>/", AdminProductDetail.as_view()),
]