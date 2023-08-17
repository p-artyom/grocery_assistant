from djoser.serializers import UserSerializer
from rest_framework.fields import SerializerMethodField

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
    # recipes = SerializerMethodField(read_only=True)
    # recipes_count = SerializerMethodField(read_only=True)

    class Met(SpecialUserSerializer.Meta):
        fields = SpecialUserSerializer.Meta.fields
        # fields = SpecialUserSerializer.Meta.fields + (
        #     'recipes',
        #     'recipes_count',
        # )

    # def get_recipes(self, object):
    #     pass

    # def get_recipes_count(self, object):
    #     pass
