from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSignUpSerializer, CompanySignUpSerializer

User = get_user_model()


class UserSignUpView(generics.GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSignUpSerializer(user, context=self.get_serializer_context()).data,
            'message': "Account successfully registered"
        })


class CompanySignUpView(generics.GenericAPIView):
    serializer_class = CompanySignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': CompanySignUpSerializer(user, context=self.get_serializer_context()).data,
            'message': "Account successfully registered"
        })


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        try:
            user = User.objects.get(email=email, activation_code=activation_code)
            user.is_active = True
            user.activation_code = ""
            user.save()
            return Response(
                {"Message": "Successfully activated."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"Message": "Wrong email."},
                status=status.HTTP_400_BAD_REQUEST
            )