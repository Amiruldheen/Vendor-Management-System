from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',views.home, name='home'),

    path('api/vendors/', views.CreateVendor.as_view()),
    path('api/vendors/<int:pk>/', views.VendorDetail.as_view()),

    path('api/purchase_orders/', views.CreatePurchaseOrder.as_view()),
    path('api/purchase_orders/<int:pk>/', views.PurchaseOrderDetail.as_view()),

    path('api/vendors/<int:pk>/performance/', views.VendorPerformance.as_view(), name='vendor-performance'),

    path('api/purchase_orders/<int:pk>/acknowledge/', views.AcknowledgePurchaseOrder.as_view(), name='acknowledge_purchase_order'),

    path('api/historical-performance/<int:pk>/', views.HistoricalPerformanceCreateView.as_view(), name='historical-performance-create'),
]