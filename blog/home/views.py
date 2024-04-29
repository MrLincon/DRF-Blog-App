from rest_framework import status
from rest_framework.views import APIView
from .models import Blog
from .serializer import BlogSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

class AddBlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):

        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong!'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'Blog created successfully!'
            }, status=status.HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Internal Server Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchBlogView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            serializer = BlogSerializer(data=blogs, many=True)

            serializer.is_valid()

            return Response({
                'data': serializer.data,
                'message': 'Data fetched successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Internal Server Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchBlogByIdView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request, uid):
        try:
            try:
                blog = Blog.objects.get(pk=uid)
            except Exception as e:
                print(e)
                return Response({
                    'data': {},
                    'message': 'Blog not found!'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = BlogSerializer(blog)

            return Response({
                'data': serializer.data,
                'message': 'Blog fetched successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Internal Server Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchBlogView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request, searched):
        try:
            blogs = Blog.objects.filter(user=request.user)

            if searched:
                blogs = blogs.filter(title__icontains=searched)

            serializer = BlogSerializer(data=blogs, many=True)

            serializer.is_valid()

            return Response({
                'data': serializer.data,
                'message': 'Data fetched successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': {},
                'message': 'Internal Server Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateBlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, uid):
        try:
            try:
                blog = Blog.objects.get(pk=uid)
            except Exception as e:
                print(e)
                return Response({
                    'data': {},
                    'message': 'Blog not found!'
                }, status=status.HTTP_404_NOT_FOUND)

            if blog.user != request.user:
                return Response({
                    'data': {},
                    'message': 'You do not have permission to update this blog.'
                }, status=status.HTTP_403_FORBIDDEN)

            serializer = BlogSerializer(blog, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'Blog updated successfully!'
                }, status=status.HTTP_200_OK)

            return Response({
                'data': serializer.errors,
                'message': 'Something went wrong!'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Internal Server Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteBlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, uid):

        try:
            try:
                blog = Blog.objects.get(pk=uid)

            except Exception as e:
                print(e)
                return Response({
                    'data': {},
                    'message': 'Blog not found!'
                }, status=status.HTTP_404_NOT_FOUND)

            if blog.user != request.user:
                return Response({
                    'data': {},
                    'message': 'You do not have permission to delete this blog!'
                }, status=status.HTTP_403_FORBIDDEN)

            # Proceed with deleting the blog
            blog.delete()
            return Response({
                'data': {},
                'message': 'Blog deleted successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)  # Log the exception for debugging
            return Response({
                'data': {},
                'message': 'Internal Server Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)