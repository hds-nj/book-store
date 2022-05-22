from django.urls import path , include
from . import views 
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', TemplateView.as_view(template_name='index.html')),
    path('', include('product.urls')),
    path('api/users/', include('account.urls')),
    # path('api/orders/', include('orders.urls')),

]