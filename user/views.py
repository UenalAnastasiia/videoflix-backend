from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from .functions import send_confirmation_email
from .models import CustomUser
import uuid
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


@api_view(['POST'])
def register_view(request):
    serializer_class = RegisterSerializer
    serializer = serializer_class(data=request.data, context={'request': request})
    token = str(uuid.uuid4())
    if serializer.is_valid(raise_exception=True):
        user = CustomUser.objects.create_user(username=request.data['username'], 
                                              email=request.data['email'], 
                                              password=request.data['password'],
                                              first_name=request.data['first_name'],
                                              last_name=request.data['last_name'],
                                              image=request.data['image'],
                                              email_confirmation_token=token, 
                                              is_active=True)
        send_confirmation_email(user, token)
        return Response({'message': 'User registered successfully. Please check your email for confirmation.'},
            status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def confirm_email_view(request, token):
    try:
        decode_token = force_str(urlsafe_base64_decode(token))
        user = CustomUser.objects.get(email_confirmation_token=decode_token)
        user.email_confirmed = True
        user.is_active = True
        user.save()
        return redirect("https://videoflix.anastasiia-uenal.de/confirm-email")
    except CustomUser.DoesNotExist:
        return redirect("https://videoflix.anastasiia-uenal.de/confirm-error")
    

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Post Request for check username and password is correct in Users DB => if coorect => Login User in System
        Check if Token Object for User exist => if not exist => create new Token Object in Tokens DB
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user.email_confirmed:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'date_joined': user.date_joined,
                    'image': user.image,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Bitte bestätigen Sie Ihre E-Mail, um sich einzuloggen.'}, status=status.HTTP_403_FORBIDDEN)
        else: Response({'error': 'Ungültige Anmeldeinformationen.'}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    def get(self, request, format=None):
        """"
        Get Request for Logout User from system
        """
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UsersViewSet(APIView):

    def get(self, request, format=None):
        receiverList = CustomUser.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'image')
        return Response(receiverList)
    

class UserDetailsViewSet(APIView):
    def get(self, request, pk):
        try:
            user = CustomUser.objects.filter(id=pk)
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        

    def get_queryset(self, pk):
        """
        Help Queryset for update user objects
        """
        try:
            user = CustomUser.objects.get(id=pk)
            return user
        except CustomUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
    
    def patch(self, request, pk, format=None):
        """
        Patch Request for Update User Object by pk in Users DB 
        """
        user = self.get_queryset(pk)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST)