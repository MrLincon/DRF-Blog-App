from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import RegisterSerializer, LoginSerializer
from rest_framework import status


class RegisterView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong!'
                }, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer.save()
                return Response({
                    'data': {},
                    'message': 'Account creation successful!'
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong!',

            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            response = serializer.get_token(serializer.data)
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong!',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
