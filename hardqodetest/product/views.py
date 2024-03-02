from django.db.models import Q, F
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .serializers import (
    ProductSerializer,
    LessonSerializer,
    StudentsGroupSerializer,
    ProductListSerializer,
    ProductLessonsSerializer,
    AdditionalTaskSerializer,
)
from .models import Product, StudentsGroup
from rest_framework import serializers
import datetime


class ProductCreateApiView(CreateAPIView):
    """
    Эндпоинт для создания нового продукта

    Методы:
        POST: Создание нового продукта

    Параметры запроса (в теле запроса в формате JSON):
        name: Название продукта
        start: Когда продукт стартует
        price: Цена продукта
        max_students: Максимальное кол-во студентов
        min_students: Минимальное кол-во студентов

    Ответ:
        201 Created: Продукт успешно создан. Возвращает сообщение о создании и идентификатор продукта (id)
        400 Bad Request: Ошибка валидации. Возвращает сообщение об ошибке
        401 Unauthorized: Ошибка авторизации
    """

    def post(self, request):
        profile = request.user.profile.status
        data = request.data
        data['start'] = datetime.datetime.strptime(data['start'], '%d.%m.%Y %H:%M')
        if request.user.is_authenticated:
            if profile == 'Учитель':
                data['teacher'] = request.user.id
                serializer = ProductSerializer(data=data)
                if serializer.is_valid():
                    try:
                        product = serializer.save()
                        return Response({'message': 'Продукт успешно создан', 'id': product.id}, status=200)
                    except serializers.ValidationError as e:
                        return Response(status=400)
                return Response({'message': serializer.errors}, status=400)
            return Response({'message': 'Создавать новый продукт могут только учителя'}, status=400)
        return Response({'message': 'Авторизуйтесь пожалуйста'}, status=401)


class LessonCreateApiView(CreateAPIView):
    """
    Эндпоинт для создания нового урока

    Методы:
        POST: Создание нового урока

    Параметры запроса (в теле запроса в формате JSON):
        name: Название урока
        link: Ссылка на видео
        product: Id продукта к которому привязан урок

    Ответ:
        201 Created: Урок успешно создан. Возвращает сообщение о создании и идентификатор продукта (id)
        400 Bad Request: Ошибка валидации. Возвращает сообщение об ошибке
        401 Unauthorized: Ошибка авторизации
    """

    def post(self, request):
        data = request.data
        serializer = LessonSerializer(data=data)
        if request.user.is_authenticated:
            if serializer.is_valid():
                lesson = serializer.save()
                return Response({'message': 'Урок успешно создан', 'id': lesson.id}, status=201)
            return Response(serializer.errors, 400)
        return Response({'message': 'Авторизуйтесь пожалуйста'}, 401)


class StudentGroupCreateView(CreateAPIView):
    """
    Эндпоинт для создания новой группы студентов.

    Метод:
        POST: Создание новой группы

    Параметры запроса (в теле запроса в формате JSON):
        name: Название группы
        product: Id продукта, к которому привязана группа

    Ответ:
        201 Created: Группа успешно создана. Возвращает сообщение о создании и идентификатор группы (id)
        400 Bad Request: Ошибка валидации. Возвращает сообщение об ошибке
    """

    def post(self, request):
        data = request.data
        serializer = StudentsGroupSerializer(data=data)
        if serializer.is_valid():
            group = serializer.save()
            return Response({'message': 'Группа успешна создана', 'id': group.id}, status=201)
        return Response(serializer.errors, status=400)


class GroupAllocation(APIView):
    """
    Эндпоинт для распределения студента в группу продукта.
    Сначала все группы заполняются до минимального кол-ва студентов,
    если студентов будет ровно столько сколько минимум в продукте для
    старта, наберется всего 1 группа, далее равномерно в каждую группу
    добавляется по 1 студенту до максимального
    значения

    Метод:
        POST: Распределение студента в группу продукта

    Параметры запроса (в теле запроса в формате JSON):
        id: Идентификатор продукта, в группу которого происходит распределение

    Ответ:
        200 OK: Успешное распределение. Возвращает сообщение об успешном доступе к продукту.
        400 Bad Request: Ошибка валидации, отсутствие продукта или отсутствие свободных мест.
                         Возвращает сообщение об ошибке.
        401 Unauthorized: Ошибка авторизации
    """

    def post(self, request):
        if request.user.is_authenticated:
            id = request.data['id']
            try:
                product = Product.objects.prefetch_related('groups').get(id=id)
            except Product.DoesNotExist:
                return Response({'message': 'Такой продукт не найден'}, status=400)
            user = request.user
            group = product.groups.filter(students=user).first()
            if group:
                return Response({'message': f'У студента с id {user.id} '
                                            f'уже есть доступ к продукту {product.name}'}, status=400)

            group = product.groups.filter(current_students__lt=F('min_students')).first()
            if group is None:
                group = product.groups.order_by('current_students').first()
            if group.max_students > group.current_students:
                group.students.add(request.user)
                group.current_students += 1
                group.save()
                return Response({'message': f'Студент с id {request.user.id} '
                                            f'успешно получил доступ к продукту {product.name},'
                                            f' записан в группу {group.name}'}, status=200)
            return Response({'message': 'У продукта не осталось групп со свободными местами'}, status=400)
        return Response({'message': 'Авторизуйтесь пожалуйста'}, status=401)


class ProductListApiView(ListAPIView):
    """
    Эндпоинт для получения списка продуктов, которые пользователь
    еще не приобрел
    """
    model = Product
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('lessons', 'teacher').filter(
            ~Q(students=self.request.user.id)).all()
        return queryset


class ProductOwnedListApiView(RetrieveAPIView):
    """
    Эндпоинт для получения деталей продукта, к которому у пользователя есть доступ.

    Параметры запроса (в URL):
        id: Идентификатор продукта

    Ответ:
        200 OK: Возвращает детали продукта
        400 Not Found: Если продукт не найден или у пользователя нет доступа к продутку
    """
    model = Product
    serializer_class = ProductLessonsSerializer
    lookup_field = 'id'

    def get_object(self):
        queryset = (Product.objects.prefetch_related('lessons', 'teacher').
                    filter(students=self.request.user, id=self.kwargs['id']).first())
        if queryset:
            return queryset
        raise serializers.ValidationError('Такого продукта нет или у вас нет к нему доступа')


class AdditionalTask(ListAPIView):
    """
    Эндпоинт отображает список продуктов со статистикой
    """
    model = Product
    serializer_class = AdditionalTaskSerializer
    queryset = Product.objects.all()
