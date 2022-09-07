from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с подписками."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Нельзя подписаться на автора более одного раза'
            )
        ]

    def validate_following(self, following):
        """Проверка подписки.

        Args:
            following (User): объект пользователя.

        Raises:
            serializers.ValidationError: ошибка при попытке подписки на самого
            себя.

        Returns:
            User: объект пользователя.
        """
        if following == self.context['request'].user:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя')
        return following


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с группами."""

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с постами."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Post
        fields = '__all__'
