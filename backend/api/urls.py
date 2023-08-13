from django.urls import include, path
from rest_framework import routers

from api.views import IngredientAPIView, RecipeAPIView, TagAPIView

router = routers.DefaultRouter()
router.register('tags', TagAPIView, basename='tags')
router.register('ingredients', IngredientAPIView, basename='ingredients')
router.register('recipes', RecipeAPIView, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),
]
