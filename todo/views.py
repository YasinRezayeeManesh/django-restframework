from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from home.models import Todo
from .serializers import TodoSerializers, UserSerializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# CRUD => Create , Read , Upgrade , Delete
# GET => دریافت اطلاعات
# POST => ارسال اطلاعات
# PUT => ویرایش اطلاعات
# DELETE => حذف اطلاعات


# region functions

@api_view(['GET', 'POST'])
def todo_ser(request: Request):
    if request.method == 'GET':
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializers(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serialize = TodoSerializers(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status.HTTP_201_CREATED)

    return Response(None, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_view(request: Request, todo_id: int):
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(None, status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializers(todo)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TodoSerializers(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)

# endregion


# region classes

class TodosListApiView(APIView):

    def get(self, request: Request):
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializers(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = TodoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        return Response(None, status.HTTP_400_BAD_REQUEST)


class TodosDetailApiView(APIView):

    def get_object(self, todo_id):
        try:
            todo = Todo.objects.get(pk=todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializers(todo)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializers(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)

# endregion


# region mixins

class TodoListMixinApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializers

    def get(self, request: Request):
        return self.list(request)

    def post(self, request: Request):
        return self.create(request)


class TodoDetailMixinView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializers

    def get(self, request: Request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request: Request, pk):
        return self.update(request, pk)
    
    def delete(self, request: Request, pk):
        return self.destroy(request, pk)

# endregion


# region generics
class TodoGenericAPIViewPagination(PageNumberPagination):
    page_size = 2


class TodoGenericListApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('id').all()
    serializer_class = TodoSerializers
    pagination_class = TodoGenericAPIViewPagination
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class TodoGenericDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('id').all()
    serializer_class = TodoSerializers

# endregion


# region viewsets

class TodosViewsSetApiView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('id').all()
    serializer_class = TodoSerializers
    pagination_class = LimitOffsetPagination

# endregion


# region users
User = get_user_model()


class UserGenericApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

# endregion
