from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user

import os
import uuid
import boto3

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, APIView

from .models import Post, Collective, Image, Event
from accounts.models import User
from .serializers import PostSerializer, CollectiveSerializer, ImageSerializer

# Create your views here.

"""
    POST VIEW FUNCTIONS
"""

class PostListCreateView(APIView):

    """
        a view for creating and listing posts
    """

    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # GET ALL POSTS AT /posts/ 'GET'
    def get(self, request:Request, *args, **kwargs):
        posts = Post.objects.all()

        # In this case, the 'instance' is going to be the data that we are returning
        # the 'many' argument will tell the serializer to return a list of data for all of the posts in our database
        serializer=self.serializer_class(instance=posts, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # ADD A NEW POST AT /posts/ 'POST'
    def post(self, request:Request, *args, **kwargs):
        data = request.data

        print('data: ', request.data)

        collective = Collective.objects.get(id=data['collective_id'])
        user = User.objects.get(id=data['user'])

        data['collective'] = collective.id
        print(user.username)
        data['username'] = user.username

        del data['collective_id']

        # self.serializer_class was defined to be PostSerializer at the top of our class view
        serializer = self.serializer_class(data=data)

        print(serializer)



        if serializer.is_valid():


            serializer.save()

            response = {
                "message": "Post Created",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        print(serializer)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        
class PostRetrieveUpdateDeleteView(APIView):

    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request:Request, post_id:int):
        post = get_object_or_404(Post, pk=post_id)

        serializer = self.serializer_class(instance=post)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request:Request, post_id:int):
        post = get_object_or_404(Post, pk=post_id)

        data = request.data

        serializer = self.serializer_class(instance=post, data=data)

        print(serializer)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "Post updated",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request:Request, post_id:int):
        post = get_object_or_404(Post, pk=post_id)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

"""
    COLLECTIVE VIEW FUNCTIONS
"""

class CollectiveListCreateView(APIView):

    serializer_class = CollectiveSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # GET ALL COLLECTIVES AT /collectives/ 'GET'
    def get(self, request:Request, *args, **kwargs):
        collectives = Collective.objects.all()

        serializer=self.serializer_class(instance=collectives, many=True)

        print(serializer.data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # ADD A NEW COLLECTIVE AT /collectives/ 'POST'
    def post(self, request:Request, *args, **kwargs):
        data = request.data

        # user = User.objects.filter(id=id)[0]

        user = User.objects.get(username=request.user).id


        data['members'] = [user]

        # print('first print ', request.data, user)

        serializer = self.serializer_class(data=data)
        # serializer.members.add(user)

        print('serializer', serializer)

        if serializer.is_valid():

            serializer.save()

            response = {
                "message": "Collective Created",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CollectiveRetrieveUpdateDeleteView(APIView):

    serializer_class = CollectiveSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request:Request, collective_id:int):
        collective = get_object_or_404(Collective, pk=collective_id)

        serializer = self.serializer_class(instance=collective)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request:Request, collective_id:int):
        collective = get_object_or_404(Collective, pk=collective_id)

        data = request.data

        serializer = self.serializer_class(instance=collective, data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "Collective updated",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request:Request, collective_id:int):
        post = get_object_or_404(Collective, pk=collective_id)

        post.delete()

        return Response(data={"message": "Collective deleted"}, status=status.HTTP_204_NO_CONTENT)
    
"""
    IMAGE VIEW FUNCTIONS
"""

@api_view(http_method_names=['POST'])
def add_image(request:Request, post_id):

    image_file = request.FILES.get('image-file', None)

    print(image_file)

    if image_file:
        s3 = boto3.client('s3')
        
        key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]

        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(image_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            post = Post.objects.get(id=post_id)
            collective = Collective.objects.get(id=post.collective.id)
            image = Image.objects.create(url=url, post=post, collective=collective)

            serializer =  ImageSerializer(instance=image, many=False)

            response = {
                "message": "Image successfully created",
                "image": serializer.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
        
        return Response(data={"message": "An error occurred uploading file to S3"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data={"message": "An error occurred uploading file to S3"}, status=status.HTTP_400_BAD_REQUEST)
        


class ImageListCreateView(APIView):

    serializer_class = ImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request:Request, *args, **kwargs):
        collectives = Collective.objects.all()

        serializer=self.serializer_class(instance=collectives, many=True)

        print(serializer.data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # ADD A NEW COLLECTIVE AT /collectives/ 'POST'
    def post(self, request:Request, *args, **kwargs):
        data = request.data

        # user = User.objects.filter(id=id)[0]

        user = User.objects.get(username=request.user).id


        data['members'] = [user]

        # print('first print ', request.data, user)

        serializer = self.serializer_class(data=data)
        # serializer.members.add(user)

        print('serializer', serializer)

        if serializer.is_valid():

            serializer.save()

            response = {
                "message": "Collective Created",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(http_method_names=['GET'])
def get_posts_by_collective(request:Request, collective_id:int):

    # returns a 404 error if the object is not found
    collective = get_object_or_404(Collective, pk=collective_id)

    posts = collective.post_set.all()
    images = collective.image_set.all()


    if len(posts):
        pserializer = PostSerializer(many=True, instance=posts)
        iserializer = ImageSerializer(many=True, instance=images)

        response = {
            "message":"Posts retrieved",
            "data": {
                "posts": pserializer.data,
                "images": iserializer.data
            }
        }

        return Response(data=response, status=status.HTTP_200_OK)

    else:
        response = {
            "message": "No posts found",
            "data": {
                "posts": pserializer.data,
                "images": iserializer.data
            }
        }

        return Response(data=response, status=status.HTTP_200_OK)

    

    # this will only run if the object has been found
    


# Collective Search
@api_view(http_method_names=['POST'])
def search_for_collective(request:Request):

    search_terms = request.data['search']

    print(search_terms)


    matching_collectives = Collective.objects.filter(name__icontains=search_terms)

    serializer = CollectiveSerializer(many=True, instance=matching_collectives)

    response = {
        "message":"post",
        "data": serializer.data
    }

    # this will only run if the object has been found
    return Response(data=response, status=status.HTTP_200_OK)
    

# Join a Collective
@api_view(http_method_names=['POST'])
def join_collective(request:Request):

    data = request.data

    collective = Collective.objects.get(id=data['collective'])
    user = User.objects.get(id=data['user'])

    collective.members.add(user)

    response = {
        "message":"Successfully joined collective",
    }

    return Response(data={'message': 'Successfully joined collective'}, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def get_user_collectives(request:Request):

    data = request.data

    user = User.objects.get(id=data['user'])

    collectives = user.collective_set.all()

    serializer = CollectiveSerializer(many=True, instance=collectives)

    response = {
        "message":"Successfully joined collective",
        "data": serializer.data
    }

    return Response(data=response, status=status.HTTP_200_OK)
