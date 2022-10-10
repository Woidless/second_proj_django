# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from . import serializers


from .permissions import IsAuthor
from main.models import Category, Favorites, Like, Post, Comment

class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 1000


''' '''
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


''' '''
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('owner', 'category')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        elif self.action == 'retrieve':
            return serializers.PostSerializer
        else:
            return serializers.PostListSerializer
        
    def get_permissions(self):
        # only author can delete and change
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        # login user can create
        elif self.action in ('create',
                            'add_to_liked',
                            'remove_from_liked',
                            'favorite_action',):
            return [permissions.IsAuthenticated()]
        # everybody can see
        else:
            return [permissions.AllowAny()]

    # posts/<id>/comments/
    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = serializers.CommentSerializers(comments, many=True)
        return Response(serializer.data, status=200)

    # posts/<id>/add_to_liked/
    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        post = self.get_object()
        user = request.user

        if user.liked.filter(post=post).exists():
            return Response('This post is already liked!', status=404)
        Like.objects.create(owner=user, post=post)
        return Response('You liked post!', status=201)

    # posts/<id>/remove_from_liked/
    @action(['DELETE'], detail=True)
    def remove_from_liked(self, request, pk):
        post = self.get_object()
        user = request.user

        if not user.liked.filter(post=post).exists():
            return Response('You didn\'t liked this post!', status=400)
        user.liked.filter(post=post).delete()
        return Response('Your like is deleted!', status=204)

    # posts/<id>/get_likes/
    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = serializers.LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)

    # posts/<id>/get_likes/
    @action(['POST'], detail=True)
    def favorite_action(self, request, pk):
        post = self.get_object()
        user = request.user
        if user.favorites.filter(post=post).exists():
            user.favorites.filter(post=post).delete()
            return Response('Deleted from FAV', status= 204)
        Favorites.objects.create(owner=user, post=post)
        return Response('Added to FAV', status=201)

''' '''
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


''' '''
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializers
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)

    def get_permissions(self):
        if self.request.method in ('GET'): return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsAuthor())
        

''' '''




''' '''
# class LikeCreateView(generics.CreateAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = serializers.LikeSerializer

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

''' '''
# class LikeDeleteView(generics.DestroyAPIView):
#     queryset = Like.objects.all()
#     permission_classes = (permissions.IsAuthenticated, IsAuthor)
    

''' '''
# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     # serializer_class = serializers.PostListSerializer
    
#     def get_serializer_class(self):
#         if self.request.method == 'GET': return serializers.PostListSerializer
#         return serializers.PostCreateSerializer
    
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

''' '''
    
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     # serializer_class = serializers.
        
#     def get_permissions(self):
#         if self.request.method in ('PUT', 'PATCH', 'DELETE'):
#             return (permissions.IsAuthenticated(), IsAuthor())
#         return (permissions.AllowAny(),)

#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return serializers.PostCreateSerializer
#         return serializers.PostSerializer
''' '''
# function based view

# @api_view(['GET'])
# def category_list(request):
#     queryset = Category.objects.all()
#     serializer = serializers.CategorySerializer(queryset, many=True)
#     return Response(data=serializer.data, status=200)


# class base view (APIvew)

# class CategoryListView(APIView):
#     def get(self, request):
#         queryset = Category.objects.all()
#         serializer = serializers.CategorySerializer(queryset, many=True)
#         return Response(data=serializer.data,status=200)

#     def post(self, request):
#         serializer = serializers.CategorySerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=201)
