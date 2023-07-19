
from rest_framework_nested import routers
from django.urls import path, include

from .views import PortfolioViewSet, InvestmentViewSet, CompanyViewSet, CustomerViewSet

router = routers.DefaultRouter()
router.register('portfolios', PortfolioViewSet, basename='portfolios')
router.register('companies', CompanyViewSet)
router.register('customers', CustomerViewSet)

portfolios_router = routers.NestedDefaultRouter(
    router, 'portfolios', lookup='portfolio')
portfolios_router.register(
    'investments', InvestmentViewSet, basename='portfolio-investments')

urlpatterns = router.urls + portfolios_router.urls
