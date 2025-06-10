from rest_framework import serializers
from home.models import Todo
from django.contrib.auth import get_user_model


User = get_user_model()


class TodoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    todos = TodoSerializers(read_only=True, many=True)

    class Meta:
        model = User
        fields = '__all__'
