# from django.contrib.auth import authenticate, login

# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import AllowAny
# from rest_framework import status
# from rest_framework.response import Response

# from .serialisers import LoginSerialiser, RegisterAdminSerialiser, RegisterUserSerialiser


# class LoginViewSet(ModelViewSet):
#     """Login View"""

#     serializer_class = LoginSerialiser
#     permission_classes = (AllowAny,)
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         # if not self.request.session.exists(self.request.session.session_key):
#         #     self.request.session.create()

#         data = request.data

#         # Ensure data is valid
#         serialiser = self.get_serializer(data=data)
#         serialiser.is_valid(raise_exception=True)

#         # Authenticate user
#         user = authenticate(request, 
#             email=serialiser.validated_data['email'], 
#             password=serialiser.validated_data['password']
#         )

#         if user is not None:
#             login(request, user)
#             return Response({'success': 'User logged in.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'User could not be authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

# class RegistrationViewSet(ModelViewSet):
#     """Registration View."""
#     serializer_class = RegisterUserSerialiser
#     permission_classes = (AllowAny,)
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         data = request.data

#         # See if a new organisation is trying to be made
#         if data.get('new_org', False) == 'True':
#             self.serializer_class = RegisterAdminSerialiser
#         else:
#             self.serializer_class = RegisterUserSerialiser

#         # Ensure data is valid
#         serialiser = self.get_serializer(data=data)
#         serialiser.is_valid(raise_exception=True)

#         # Create user and login
#         user = serialiser.save()
#         login(request, user)

#         return Response({'success': 'User created.'}, status=status.HTTP_200_OK)