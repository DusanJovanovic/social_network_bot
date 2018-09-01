import json
from django.db.models import Count
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core import serializers

from django.contrib.auth import login, authenticate

from .verification import verify
from .serializers import AccountSerializer, PostSerializer
from .models import Account, Post, Like


class AuthRegister(APIView):


    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        data = request.data
        email = request.data['email']

        # Getting data from verification
        data['first_name'], data['last_name'], data['email_verified'] = verify(email)

        serializer = AccountSerializer(data=request.data)

        # Save data into db and return 200 if data is valid 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If data is not valid return bad request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePost(APIView):

     
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        data = request.data

        # Get user id
        data['creator'] = request.user.id
        serializer = PostSerializer(data=data)

        # Save data into db and return 200 if data is valid 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If data is not valid return bad request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikePost(APIView):

     
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, post_id):

        # Get post from db
        post = Post.objects.get(post_id=post_id)
        user_id = request.user.id

        # If user is creator return bad request
        # User can not like own post
        if post.creator == user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Return bad request if user already liked post
        query_set = Like.objects.filter(post=post_id, liker=user_id)
        if len(query_set) > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Create like
        like = Like.objects.create(post=post, liker=request.user)

        # Increase like counter in post
        post.no_of_likes += 1
        post.save()

        # Return 200 with additional data
        response = {
            'post_id': post.post_id,
            'no_of_likes': post.no_of_likes,
            'creator': post.creator.id
            }
        return Response(response, status=status.HTTP_200_OK)



class UnlikePost(APIView):

     
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, post_id):

        # Retrive post object and user id
        post = Post.objects.get(post_id=post_id)
        user_id = request.user.id

        # Return bad request if user and creator of the post are the same
        if post.creator == user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Return bad request if user did not like the post previously
        query_set = Like.objects.filter(post=post_id, liker=user_id)
        if len(query_set) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
        # Delete(unlike) the like of a post and return 200
        query_set[0].delete()
        return Response(status=status.HTTP_200_OK)


class GetUsersWithZeroLike(APIView):

     
    permission_classes = (AllowAny,)

    def get(self, request):

        # Return a list of users with posts with zero likes
        get_all_users = Post.objects.filter(no_of_likes=0).values_list('creator', flat=True).distinct()
        return Response(get_all_users, status=status.HTTP_200_OK)



class GetUsersByPosts(APIView):

     
    permission_classes = (AllowAny,)

    def get(self, request):

        # Return json with users and number of posts by each user
        get_all_creators = Post.objects.values('creator').annotate(dcount=Count('creator'))
        d = {x['creator']: x['dcount'] for x in get_all_creators}
        return Response(d, status=status.HTTP_200_OK)


class GetPostsByUser(APIView):

    
    permission_classes = (AllowAny,)

    def get(self, request, user_id):
        
        # Get list of all posts by user
        get_all_posts = Post.objects.filter(creator=user_id).values_list('pk', flat=True)
        #serialized_queryset = serializers.serialize('json', get_all_posts)
        return Response(get_all_posts, status=status.HTTP_200_OK)

