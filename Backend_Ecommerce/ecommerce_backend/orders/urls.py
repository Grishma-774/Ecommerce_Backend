
from django.urls import path
from .views import OrderViews,GetOrderHistory,GetOrderDetails,AdminAllOrders,AdminUpdateOrders,AdminGetOrderDetails

urlpatterns = [

    path("orderitems/",OrderViews.as_view()),
    path("get_order/history/",GetOrderHistory.as_view()),
    path("get_order_details/<int:pk>",GetOrderDetails.as_view()),
    path("admin/all_orders/",AdminAllOrders.as_view()),
    path("admin/order_details/<int:pk>/",AdminGetOrderDetails.as_view()),
    path("admin/orders/<int:pk>/",AdminUpdateOrders.as_view())
    
]