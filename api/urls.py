from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'api'
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename="brands")
router.register(r'stores', StoreViewSet, basename="stores")
router.register(r'deals', DealViewSet, basename="deals")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls), name='api'),
    path('auth', AuthView.as_view(), name='auth'),
    path('suscription', SuscriptionStore.as_view(), name='suscription'),
    path('suscription-users', SuscriptionUsers.as_view(), name='suscription-users'),
]