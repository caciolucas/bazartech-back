# from authentication.utils import send_forget_password_email
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from authentication.filters import UserFilter
from authentication.models import User
from authentication.permissions import OwnAccountPermission
from authentication.serializers import UserSerializer

# Create your views here.


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ["name"]
    filterset_class = UserFilter
    permission_classes = [OwnAccountPermission]

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        User = get_user_model()
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data)
        else:
            return Response(user.errors, status=400)


# TODO: Enable the reset password feature with a better template
# class ResetPasswordView(APIView):
#     authentication_classes = []  # disables authentication
#     permission_classes = []  # disables permission

#     def post(self, request, *args, **kwargs):
#         try:
#             cpf = request.data.get("cpf")
#             user = User.objects.get(cpf=cpf)
#             new_password = datetime.now().strftime("%H%M%S")
#             user.set_password(new_password)
#             user.save()
#             send_forget_password_email(new_password, user.email)
#             return Response({"message": "Senha resetada com sucesso."})
#         except User.DoesNotExist:
#             return Response({"message": "Usuário não encontrado."}, status=404)
