from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet


app_name = 'api'

router_ver1 = routers.DefaultRouter()
router_ver1.register(r'posts', PostViewSet, basename='post')
router_ver1.register(r'groups', GroupViewSet, basename='group')
router_ver1.register(r'posts/(?P<post_id>\d+)/comments',
                     CommentViewSet,
                     basename='comments')
router_ver1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [path('v1/', include(router_ver1.urls)),
               # управление пользователями отключено в соответствии с ТЗ
               # path('v1/', include('djoser.urls')),
               path('v1/', include('djoser.urls.jwt')), ]
