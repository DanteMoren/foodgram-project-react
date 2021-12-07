from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
# def signup(request):
#     if request.method == 'POST':
#         serializer = SignupSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             if not User.objects.filter(username=request.data['username'],
#                                        email=request.data['email']).exists():
#                 if User.objects.filter(
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
#             confirmation_code = default_token_generator.make_token(user)
#             user.email_user(subject='Сonfirmation code',
#                             message=f'Code is {confirmation_code}',
#                             from_email='administration@yamdb.com')
#             return Response(serializer.data, status=status.HTTP_200_OK)
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
