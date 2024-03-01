from django.urls import path
from .views import (
    ProductCreateApiView,
    LessonCreateApiView,
    StudentGroupCreateView,
    GroupAllocation,
    ProductListApiView,
    ProductOwnedListApiView,
    AdditionalTask,
)


urlpatterns = [
    path('add-product', ProductCreateApiView.as_view(), name='add-product'),
    path('add-lesson', LessonCreateApiView.as_view(), name='add-lesson'),
    path('add-group', StudentGroupCreateView.as_view(), name='add-group'),
    path('group-allocation', GroupAllocation.as_view(), name='group-allocation'),
    path('product-list', ProductListApiView.as_view(), name='product-list'),
    path('owned-product/<int:id>', ProductOwnedListApiView.as_view(), name='owned'),
    path('additional-task', AdditionalTask.as_view(), name='additional-task')
]