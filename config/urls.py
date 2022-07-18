"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import rest_framework
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from apps.orders.views.order import OrderViewSet
from apps.terminals.views.catalog import CatalogViewSet, ProductSampleFileView
from apps.terminals.views.product import ProductViewSet
from apps.terminals.views.terminal import TerminalViewSet
from apps.transactions.views.payment import PaymentViewSet
from apps.transactions.views.transaction import TransactionViewSet
from apps.users.views import UserViewSet
from apps.users.views.statistic import StatisticViewSet

swagger_info = openapi.Info(
    title="Eureka API",
    default_version="v1",
    description="""Eureka project.""",
    contact=openapi.Contact(email="dotheduybk@gmail.com"),
    license=openapi.License(name="Private"),
)

schema_view = get_schema_view(
    info=swagger_info,
    public=True,
    authentication_classes=[
        rest_framework.authentication.SessionAuthentication
    ],
    permission_classes=[permissions.IsAdminUser],
)

api_router = SimpleRouter(trailing_slash=False)

# users
api_router.register("users", UserViewSet, basename="users")
# ---------
api_router.register("orders", OrderViewSet, basename="orders")
api_router.register("terminals", TerminalViewSet, basename="terminals")
api_router.register("payments", TransactionViewSet, basename="payments")
api_router.register("products", ProductViewSet, basename="products")
api_router.register("after-payment", PaymentViewSet, basename="after-payment")
api_router.register("workload", CatalogViewSet, basename="workload")
api_router.register("statistic", StatisticViewSet, basename="statistic")

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"api/v1/", include(api_router.urls)),
    path('product-sample-file', ProductSampleFileView.as_view(), name='product-sample-file'),
]

urlpatterns.extend([
    path(
        r"swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
])
