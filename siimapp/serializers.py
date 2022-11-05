from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from siimapp.models import Post


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        write_only_fields = 'password'
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        


class PostSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)
    
    class Meta:
        model = Post
        fields  = ['id', 'title', 'description', 'image']

