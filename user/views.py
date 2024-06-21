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
    """
    API view for registering a new user.

    This view accepts POST requests and creates a new user in the database,
    validates the entries with the RegisterSerialiser and sends a confirmation email.

    Args:
        request (HttpRequest): The HTTP request with the user data.

    Returns:
        Response: An HTTP response indicating the success or failure of the registration.
    """
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
        return Response({'message': 'User registered successfully. Please check your email for confirmation.'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def confirm_email_view(request, token):
    """
    API view for confirming a user's email address.

    This view accepts GET requests with a confirmation token,
    decodes the token, finds the corresponding user in the database,
    confirms the user's email address and redirects the user to the relevant page.

    Args:
        request (HttpRequest): The HTTP request with the confirmation token.
        token (str): The confirmation token for the user's email address.

    Returns:
        HttpResponseRedirect: A redirect of the user to the confirmation page.
    """
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
    """
    Customisation of the ObtainAuthToken class for the API view for logging in a user.
    """
    def post(self, request, *args, **kwargs):
        """
        POST request to check the user name and password in the user database.
        If correct, the user is logged in.
        Checks whether a token object exists for the user; if not, a new one is created.
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
        else: 
            Response({'error': 'Ungültige Anmeldeinformationen.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    API view for logging out a user.
    """
    def get(self, request, format=None):
        """
        GET request to log the user out of the system.
        """
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UsersViewSet(APIView):
    """
    API view for retrieving a list of user objects.
    """
    def get(self, request, format=None):
        """
        GET request to retrieve all users in the database.
        """
        receiverList = CustomUser.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'image')
        return Response(receiverList)


class UserDetailsViewSet(APIView):
    """
    API view for displaying and updating user details.
    """
    def get(self, request, pk):
        """
        GET request to retrieve the details of a specific user based on their ID (pk).
        """
        try:
            user = CustomUser.objects.filter(id=pk)
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get_queryset(self, pk):
        """
        Helper Query Set for updating user objects.
        """
        try:
            user = CustomUser.objects.get(id=pk)
            return user
        except CustomUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 

    def patch(self, request, pk, format=None):
        """
        PATCH request to update a user object based on its ID (pk).
        """
        user = self.get_queryset(pk)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST)
