from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.paginations import LimitPagination
from users.models import Subscribe, User
from users.serializers import SpecialUserSerializer, SubscribeSerializer


class SpecialUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = SpecialUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitPagination

    @action(
        methods=('POST', 'DELETE'),
        detail=True,
    )
    def subscribe(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        subscribe = Subscribe.objects.filter(user=user, following=following)
        if request.method == 'POST':
            if subscribe.exists():
                return Response(
                    {'error': 'Нельзя подписаться повторно на одного автора!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user == following:
                return Response(
                    {'error': 'Нельзя подписаться на самого себя!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = SubscribeSerializer(
                following,
                context={'request': request},
            ).data
            Subscribe.objects.create(user=user, following=following)
            return Response(serializer, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if subscribe.exists():
                subscribe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Вы не подписаны на этого автора!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        subscriptions = SubscribeSerializer(
            self.paginate_queryset(
                User.objects.filter(following__user=request.user),
            ),
            many=True,
            context={'request': request},
        ).data
        return self.get_paginated_response(subscriptions)
