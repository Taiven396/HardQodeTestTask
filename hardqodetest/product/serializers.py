from rest_framework import serializers
from .models import Product, Lesson, StudentsGroup
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'start', 'price', 'max_students', 'teacher', 'min_students']

    def create(self, validated_data):
        try:
            product = Product.objects.create(**validated_data)
            return product
        except:
            raise serializers.ValidationError('Такой продукт уже существует.')


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['name', 'link', 'product']


class StudentsGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentsGroup
        fields = ['name', 'product']

    def validate(self, validated_data):
        if len(validated_data) != 2 and ('name', 'product') not in validated_data:
            raise serializers.ValidationError('Ошибка валидации, должны быть поля "name", "product"')
        return validated_data


class ProductListSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'teacher', 'start', 'price', 'lessons']

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return [
            {
                'name': lesson.name
            }
            for lesson in lessons
        ]

    def get_teacher(self, obj):
        teacher = obj.teacher
        return {
                'name': teacher.__str__()
        }


class ProductLessonsSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['lessons']

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return [
            {
                'name': lesson.name
            }
            for lesson in lessons
        ]


class AdditionalTaskSerializer(serializers.ModelSerializer):
    total_students = serializers.SerializerMethodField()
    group_fullness = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'total_students', 'group_fullness', 'purchase_percentage']

    def get_total_students(self, obj):
        groups = obj.groups.all()
        total = 0
        for group in groups:
            total += group.students.count()
        return total

    def get_group_fullness(self, obj):
        max_students = obj.max_students
        groups = obj.groups.all()
        total = 0
        for group in groups:
            total += group.students.count()
        result = round(((total / max_students) * 100), 2)
        return f'{result} %'

    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        groups = obj.groups.all()
        total = 0
        for group in groups:
            total += group.students.count()
        result = round(((total / total_users) * 100), 2)
        return f'{result} %'
