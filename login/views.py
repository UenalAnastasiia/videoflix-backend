from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
