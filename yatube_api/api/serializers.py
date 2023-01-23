from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        read_only=False, required=True, slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')

    validators = [
        UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=('user', 'following'),
            message='Подписка на этого автора уже существует',
        )
    ]

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError('Нельзя подписаться на '
                                              'самого себя!')
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Нельзя подписаться на '
                                              'несуществующего автора!')
        # проверка работает, но все равно не решает проблему
        # видимо раньше на этапе создания кверисета поля вылезает raise error
        # "following": [
        #         "Object with username=user5 does not exist."
        #     ]
        # существует способ это побороть?
        return value
