from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.TodosViewsSetApiView)

urlpatterns = [
    path('', views.todo_ser),
    path('<int:todo_id>', views.todo_detail_view),
    path('cbv/', views.TodosListApiView.as_view()),
    path('cbv/<int:todo_id>', views.TodosDetailApiView.as_view()),
    path('mixins/', views.TodoListMixinApiView.as_view()),
    path('mixins/<pk>', views.TodoDetailMixinView.as_view()),
    path('generics/', views.TodoGenericListApiView.as_view()),
    path('generics/<pk>', views.TodoGenericDetailApiView.as_view()),
    path('viewsets/', include(router.urls)),
    path('users/', views.UserGenericApiView.as_view()),
]
