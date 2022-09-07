from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, Group,
                          GroupSerializer, Post, PostSerializer)


class ListCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Класс примесь для вывода списка и создания объекта."""

    pass


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Сохраняет текущего пользователя в качестве автора при создании
        поста.

        Args:
            serializer (PostSerializer): объект сериализатора для работы с
            постами.
        """

        serializer.save(author=self.request.user)


class FollowViewSet(ListCreateViewSet):
    """ViewSet для работы с подписками."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        """Сохраняет текущего пользователя в качестве подписчика при создании
        подписки.

        Args:
            serializer (FollowSerializer): объект сериализатора для работы с
            подписками.
        """

        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Получает список подписок.

        Returns:
            QuerySet: список подписок.
        """

        return self.request.user.follower.all()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_post(self):
        """Получает объект текущего поста.

        Returns:
            Post: объект текущего поста.
        """

        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Получает список комментариев текущего поста.

        Returns:
            QuerySet: список комментариев текущего поста.
        """

        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Сохраняет текущего пользователя в качестве автора и текущий пост
        в качестве поста при создании комментария.

        Args:
            serializer (CommentSerializer): объект сериализатора для работы с
            комментариями.
        """

        serializer.save(author=self.request.user, post=self.get_post())
