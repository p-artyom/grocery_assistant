from django.urls import include, path
from rest_framework import routers

from api.views import (
    TagAPIView
)

# router = routers.DefaultRouter()
# router.register('tags', TagAPIView, basename='tags')

urlpatterns = [
    # path('', include(router.urls)),
    path('tags/', TagAPIView.as_view(), name='get_tags')
]