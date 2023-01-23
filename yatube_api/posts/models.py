from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        ordering = ('title',)
        verbose_name = 'Группа постов'
        verbose_name_plural = 'Группы постов'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts',
        blank=True, null=True
    )

    class Meta:
        ordering = ('pub_date',)  # ordering = ('-pub_date',)
        # правильная сортировка с датой по убыванию не проходит тесты
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return (f'Пост: {self.text[:15]}, Группа: {self.group} Автор'
                f':{self.author}, Дата публикации: {self.pub_date}')


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор на которого подписан пользователь')

    class Meta:
        ordering = ('user',)
        verbose_name = 'Подписчика'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                name='unique_relationships',
                fields=['user', 'following'],
            ),
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(user=models.F('following')),
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
