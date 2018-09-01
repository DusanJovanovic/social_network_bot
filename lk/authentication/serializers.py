from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from .models import Account, Post


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'email', 'first_name', 'last_name', 'email_verified', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

class PostSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Post
        fields = ('content', 'creator', 'no_of_likes')
