
from django.urls import path
from .views import CartAddView,CartGetView,UpdateQuantityView,DeleteCartItem,DeleteAllCartItem


urlpatterns = [

    path("cart_add/",CartAddView.as_view()),
    path("cart_get/",CartGetView.as_view()),
    path("items/<int:pk>/",UpdateQuantityView.as_view()),
    path("items/delete/<int:pk>/", DeleteCartItem.as_view() ),
    path("cartItem/delete/",DeleteAllCartItem.as_view())
    
]