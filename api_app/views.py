from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, APIView


from .models import Post, Collectiv, Comment
from accounts.models import User
from .serializers import PostSerializer, CollectivSerializer, CommentSerializer

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

        collectiv = Collectiv.objects.get(id=data['collectiv_id'])
        user = User.objects.get(id=data['user'])

        data['collectiv'] = collectiv.id
        print(user.username)
        data['username'] = user.username

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

        return Response(data={"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
    
"""
    COMMENT VIEW FUNCTIONS
"""


"""
    COLLECTIV VIEW FUNCTIONS
"""

class CollectivListCreateView(APIView):

    serializer_class = CollectivSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # GET ALL COLLECTIVS AT /collectivs/ 'GET'
    def get(self, request:Request, *args, **kwargs):
        collectivs = Collectiv.objects.all()

        serializer=self.serializer_class(instance=collectivs, many=True)

        print(serializer.data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # ADD A NEW COLLECTIV AT /collectivs/ 'POST'
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
                "message": "Collectiv Created",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CollectivRetrieveUpdateDeleteView(APIView):

    serializer_class = CollectivSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request:Request, collectiv_id:int):
        collectiv = get_object_or_404(Collectiv, pk=collectiv_id)

        serializer = self.serializer_class(instance=collectiv)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request:Request, collectiv_id:int):
        collectiv = get_object_or_404(Collectiv, pk=collectiv_id)

        data = request.data

        serializer = self.serializer_class(instance=collectiv, data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "Collectiv updated",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request:Request, collectiv_id:int):
        post = get_object_or_404(Collectiv, pk=collectiv_id)

        post.delete()

        return Response(data={"message": "Collectiv deleted"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(http_method_names=['GET'])
def get_posts_by_collectiv(request:Request, collectiv_id:int):

    # returns a 404 error if the object is not found
    collectiv = get_object_or_404(Collectiv, pk=collectiv_id)

    posts = collectiv.post_set.all()

    serializer = PostSerializer(many=True, instance=posts)

    response = {
        "message":"post",
        "data": serializer.data
    }

    # this will only run if the object has been found
    return Response(data=response, status=status.HTTP_200_OK)


# Collectiv Search
@api_view(http_method_names=['POST'])
def search_for_collectiv(request:Request):

    search_terms = request.data['search']

    print(search_terms)


    matching_collectivs = Collectiv.objects.filter(name__icontains=search_terms)

    serializer = CollectivSerializer(many=True, instance=matching_collectivs)

    response = {
        "message":"post",
        "data": serializer.data
    }

    # this will only run if the object has been found
    return Response(data=response, status=status.HTTP_200_OK)
    

# Join a Collectiv
@api_view(http_method_names=['POST'])
def join_collectiv(request:Request):

    data = request.data

    collectiv = Collectiv.objects.get(id=data['collectiv'])
    user = User.objects.get(id=data['user'])

    collectiv.members.add(user)

    response = {
        "message":"Successfully joined collectiv",
    }

    return Response(data={'message': 'workin on it'}, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def get_user_collectivs(request:Request):

    data = request.data

    user = User.objects.get(id=data['user'])

    collectivs = user.collectiv_set.all()

    serializer = CollectivSerializer(many=True, instance=collectivs)

    response = {
        "message":"Successfully joined collectiv",
        "data": serializer.data
    }

    return Response(data=response, status=status.HTTP_200_OK)

"""
    CHANGE THIS TO GET USER POSTS
"""

# @api_view(http_method_names=['GET'])
# def post_detail(request:Request, post_id:int):

#     # returns a 404 error if the object is not found
#     post = get_object_or_404(Post, pk=post_id)

#     serializer = PostSerializer(instance=post)

#     response = {
#         "message":"post",
#         "data": serializer.data
#     }

#     # this will only run if the object has been found
#     return Response(data=response, status=status.HTTP_200_OK)