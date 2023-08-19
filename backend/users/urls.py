from django.urls import include, path
from rest_framework import routers

from users.views import SpecialUserViewSet

router = routers.DefaultRouter()
router.register('users', SpecialUserViewSet, basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
