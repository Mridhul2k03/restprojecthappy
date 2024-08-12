"""
URL configuration for restproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
# restproject/urls.py

from restapp.views import (
    ProductViewSet, ReviewViewSet, UserCartViewSet, CartItemViewSet, 
    RegisterView, OrderViewSet, SendEmailView, 
    CreateRazorpayOrderView, CaptureRazorpayPaymentView,ProductsVirtualViewSet
)


router = DefaultRouter()
router.register(r'products', ProductViewSet,basename='product')
router.register(r'reviews', ReviewViewSet,basename='review')
router.register(r'cart', UserCartViewSet,basename='cart')
router.register(r'cart-items', CartItemViewSet,basename='cartitem')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'products-virtual', ProductsVirtualViewSet, basename='productvirtual')
# router.register(r'order-items', OrderItemViewSet, basename='orderitem')


urlpatterns = [
    path("admin/", admin.site.urls, name=""),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
    path('auth/', include('dj_rest_auth.urls')),  # for auth endpoints
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # for registration endpoints
    path('auth/google/', include('allauth.socialaccount.urls')),  # for Google auth
    # google authentication
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('dj-rest-auth/social/', include('allauth.socialaccount.urls')),
    path('send/email/', SendEmailView.as_view(), name='send_email'),

    # razorpay
    path('create-order/', CreateRazorpayOrderView.as_view(), name='create_razorpay_order'),
    path('capture-payment/', CaptureRazorpayPaymentView.as_view(), name='capture_razorpay_payment'),
    # path('webhook/', razorpay_webhook, name='razorpay_webhook'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)