from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from djoser.views import TokenCreateView as DjoserTokenCreateView
from djoser.views import TokenDestroyView as DjoserTokenDestroyView
from .serializers import UserSerializer
from djoser.conf import settings
from djoser import utils


class TokenCreateView(DjoserTokenCreateView):
    
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_201_CREATED
        )


class TokenDestroyView(DjoserTokenDestroyView):
    
    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)
        
    # filter_backends = [filters.SearchFilter, ]
    # lookup_field = 'username'
    # search_fields = ['=username', ]

    # @action(detail=False,
    #         methods=['get', 'patch'],
    #         permission_classes=(IsAuthenticated, ))
    # def me(self, request):
    #     user = request.user
    #     if request.method == 'GET':
    #         serializer = self.get_serializer(user,)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     if request.method == 'PATCH':
    #         serializer = self.get_serializer(user, request.data, partial=True)
    #         if serializer.is_valid():
    #             if (user.role != User.ADMIN
    #                     or user.is_superuser is not True):
    #                 serializer.validated_data.pop('role', False)
    #                 serializer.update(instance=user,
    #                                   validated_data=serializer.validated_data)
    #             else:
    #                 serializer.update(instance=user,
    #                                   validated_data=serializer.validated_data)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return None


# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             if User.objects.filter(password=request.data['password'],
#                                        email=request.data['email']).exists():
#                 if not User.objects.filter(
#                     username=request.data['username']
#                 ).exists():
#                     return Response(
#                         {'error': 'invalid email'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#                 elif User.objects.filter(email=request.data['email']).exists():
#                     return Response(
#                         {'error': 'invalid username'},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#                 else:
#                     serializer.save()
#             user = User.objects.get(username=request.data['username'],
#                                     email=request.data['email'])
#             token = AccessToken.for_user(user)
#             return Response({}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @api_view(['POST'])
# def token(request):
#     if request.method == 'POST':
#         serializer = TokenSerializer(data=request.data)
#         if serializer.is_valid():
#             user = get_object_or_404(User, username=request.data['username'])
#             confirmation_code = request.data['confirmation_code']
#             if default_token_generator.check_token(user, confirmation_code):
#                 token = AccessToken.for_user(user)
#                 response = {'username': request.data['username'],
#                             'token': str(token)}
#                 return Response(response, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
