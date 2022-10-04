from rest_framework import serializers
from django.contrib.auth.models import User

class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",'username',)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        # fields = [elem for elem in '__all__' if elem != 'password']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8,
                                        write_only=True,
                                        required=True)
    password2 = serializers.CharField(min_length=8,
                                        write_only=True,
                                        required=True)
    first_name = serializers.CharField(max_length=50,
                                        required=True)
    last_name = serializers.CharField(max_length=50,
                                        required=True)

    class Meta:
        model = User
        fields = ('username', 'email',
                'first_name', 'last_name',
                'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if password2 != attrs['password']:
            raise serializers.ValidationError('Password didn\'t match')
        if not attrs['first_name'].istitle():
            raise serializers.ValidationError('Name must start with uppercase')
        return attrs
    
    def create(self, validated_data):
        # user = User.objects.create(
        #     username=validated_data('username'),
        #     first_name=validated_data('first_name'),
        #     last_name=validated_data('last_name'),
        #     email=validated_data('email'),
        # )
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user