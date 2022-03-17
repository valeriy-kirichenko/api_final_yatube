from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return (
            f'{self.pk} {self.text[:15]} {self.pub_date} '
            f'{self.author.get_username()} {self.group}'
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow')
        ]

    def clean(self):
        if self.user == self.following:
            raise ValidationError('Вы не можете подписаться на самого себя')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
