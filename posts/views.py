from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Tag
from .serializers import PostSerializers, TagSerializers, SignupSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    @swagger_auto_schema(
        operation_description="Create a new user and return JWT tokens",
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                    }),
                    'tokens': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    }),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)

# class PostViewset(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializers

class PostView(APIView):
    """
    The PostView class is a view that handles the creation of new posts and getting all posts.
    """
    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=PostSerializers,
        responses={201: PostSerializers, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = PostSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Get all posts with optional filtering and search",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING),
            openapi.Parameter('author', openapi.IN_QUERY, description="Filter by author ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('tag', openapi.IN_QUERY, description="Filter by tag ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search in title, content, author username", type=openapi.TYPE_STRING),
        ],
        responses={200: PostSerializers(many=True)}
    )
    def get(self, request):
        posts = Post.objects.select_related('author').prefetch_related('tag').all()
        filter_backends = [DjangoFilterBackend, filters.SearchFilter]
        filter_fields = ['title', 'author', 'tag']
        search_fields = ['title', 'content', 'author__username']
        serializer = PostSerializers(posts, many = True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    
class PostUpdateDeleteView(APIView):
    """
    The PostUpdateDeleteView class is a view that handles the updating and deleting of posts.
    """
    @swagger_auto_schema(
        operation_description="Update a post entirely",
        request_body=PostSerializers,
        responses={200: PostSerializers, 400: "Bad Request"}
    )
    def put(self, request, pk):
        posts = Post.get_object(pk)
        serializer = PostSerializers(posts, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a post",
        request_body=PostSerializers,
        responses={200: PostSerializers, 400: "Bad Request"}
    )
    def patch(self, request, pk):
        posts = Post.get_object(pk)
        serializer = PostSerializers(posts, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a post",
        responses={204: "No Content"}
    )
    def delete(self, request, pk):
        posts = Post.get_object(pk)
        posts.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class TagView(APIView):
    """
    The TagView class is a view that handles the creation of new tags and getting all tags.
    """
    @swagger_auto_schema(
        operation_description="Create a new tag",
        request_body=TagSerializers,
        responses={201: TagSerializers, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = TagSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Get all tags with optional filtering and search",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
        ],
        responses={200: TagSerializers(many=True)}
    )
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializers(tags, many = True)
        return Response(serializer.data, status.HTTP_200_OK)



        

