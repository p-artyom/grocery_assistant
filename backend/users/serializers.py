from djoser.serializers import UserSerializer
from rest_framework.fields import SerializerMethodField

from api import serializers
from recipes.models import Recipe
from users.models import Subscribe, User


class SpecialUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=user,
            following=object.id,
        ).exists()


class SubscribeSerializer(SpecialUserSerializer):
    recipes = SerializerMethodField(
        read_only=True,
    )
    recipes_count = SerializerMethodField(
        read_only=True,
    )

    class Meta(SpecialUserSerializer.Meta):
        fields = SpecialUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, object):
        del object
        return True

    def get_recipes(self, object):
        recipes = Recipe.objects.filter(author=object)
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        recipes = serializers.RecipeInActionSerializer(
            recipes,
            many=True,
        ).data
        return recipes

    def get_recipes_count(self, object):
        return Recipe.objects.filter(author=object).count()
