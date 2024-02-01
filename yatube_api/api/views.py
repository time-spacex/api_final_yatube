from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Follow, Group, Post
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
from .permissions import OwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет API для модели постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        """Метод API для создания постов."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет API для модели групп постов."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (OwnerOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет API для модели комментариев к постам."""

    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self):
        """Метод API для получения querysetа комметариев."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        """Метод API для создания комментария."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewset(viewsets.ModelViewSet):
    """Вьюсет API для модели подписок пользователей."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Метод API для получения querysetа подписок."""
        return Follow.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Метод API для создания подписок."""
        serializer.save(user=self.request.user)
