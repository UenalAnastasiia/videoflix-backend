from django.http import JsonResponse
from odf.table import ErrorMessage
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer
from .functions import send_confirmation_email
from user.models import CustomUser
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
                                              email_confirmation_token=token, 
                                              is_active=False)
        send_confirmation_email(user, token)
        return JsonResponse({'message': 'User registered successfully. Please check your email for confirmation.'})
    else:
        return JsonResponse(ErrorMessage, status=400) 


@api_view(['GET'])
def confirm_email_view(request, token):
    try:
        decode_token = force_str(urlsafe_base64_decode(token))
        user = CustomUser.objects.get(email_confirmation_token=decode_token)
        user.email_confirmed = True
        user.is_active = True
        user.save()
        return JsonResponse({'message': 'Your email has been confirmed. You can now log in.'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Invalid confirmation token.'})
    

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
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else: Response(serializer.errors)