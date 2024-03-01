from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout


class UserCreationApiView(CreateAPIView):
    """
    Эндпоинт для создания нового пользователя

    Методы:
        POST: Создание нового пользователя

    Параметры запроса (в теле запроса в формате JSON):
        username: Имя пользователя
        password: Пароль пользователя
        password_confirm: Подтверждение пароля (должно совпадать с паролем)

    Ответ:
        201 Created: Пользователь успешно создан. Возвращает сообщение о создании и идентификатор пользователя (id)
        400 Bad Request: Ошибка валидации. Возвращает сообщение об ошибке
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({'message': 'Пользователь создан', 'id': f"{user.id}"}, status=201)
        return Response(serializer.errors, status=400)


class SingIn(APIView):
    """
    Эндпоитн для входа пользователя

    Методы:
        POST: Вход пользователя

    Параметры запроса (в теле запроса в формате JSON):
        username: Имя пользователя
        password: Пароль пользователя

    Ответ:
        200 Ok: Успешный вход
        401 Unauthorized: Неверные данные аккаунта
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print(request.user)
        if user is None:
            return Response({'message': 'Пользователь с таким именем или паролем не найден'}, status=401)
        login(request, user)
        return Response({'message': 'Успешный вход'}, status=200)


class Logout(APIView):
    """
    Эндоинт для выхода пользователя

    Методы:
        GET: Выход пользователя

    Ответ:
        200 Ok: Успешный выход
        401 Unauthorized: Пользователь не авторизован
    """
    def get(self, request):
        print(request.user)
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Успешный выход'}, status=200)
        return Response({'message': 'Вы не авторизованы'}, status=401)
