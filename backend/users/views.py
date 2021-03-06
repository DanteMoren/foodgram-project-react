from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView

from api.pagination import LimitPageNumberPagination
from api.serializers import FollowSerializer
from users.models import Follow

User = get_user_model()


class TokenCreateView(DjoserTokenCreateView):

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class TokenDestroyView(DjoserTokenDestroyView):

    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': 'Вы не можете подписаться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({
                'errors': 'Вы не можете отписаться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы не были подписаны или уже отписались от пользователя'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
