from unicodedata import category
from urllib import request
from rest_framework import serializers
from .models import Category, Favorites, Like, Post, Comment, PostImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'preview',)
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['likes_count'] = instance.likes.count()
        return repr


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        exclude = ('id', 'title')


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=False, required=False)
    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'preview', 'images')
    
    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        images_objects = [PostImage(post=post, image=image) for image in images_data]
        PostImage.objects.bulk_create(images_objects)
        return post


class CommentSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # post = serializers.ReadOnlyField(source='post.title')
    
    class Meta:
        model = Comment
        fields = ('id', 'body', 'post', 'owner')


class PostSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    owner = serializers.ReadOnlyField(source='owner.username')
    images = PostImageSerializer(many=True)
    comments = CommentSerializers(many=True)

    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ('owner', 'post')


class FvorateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('post',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['posts'] = PostListSerializer(instance.post).data
        return repr
