from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app_affiliate.api.views import AffiliateViewSet, ContributionViewSet

router = DefaultRouter()
router.register(r'affiliates', AffiliateViewSet, basename='affiliate')
router.register(r'contributions', ContributionViewSet, basename='contribution')

urlpatterns = [
    path('', include(router.urls)),
]
