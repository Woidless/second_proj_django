# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from . import serializers
from .permissions import IsAuthor
from main.models import Category, Post

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

        
# 

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # serializer_class = serializers.PostListSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET': return serializers.PostListSerializer
        return serializers.PostCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    # serializer_class = serializers.
    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return serializers.PostCreateSerializer
        return serializers.PostSerializer
        
    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return (permissions.IsAuthenticated(), IsAuthor())
        return (permissions.AllowAny(),)

