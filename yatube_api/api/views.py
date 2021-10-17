from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post

from .permissions import AuthorEditOrReadOnly
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorEditOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get']


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorEditOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        return comments

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post_id = self.kwargs.get("post_id")
        get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user)
