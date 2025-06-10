from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

user = get_user_model()

class Todo(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    priority = models.IntegerField(default=1)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='todos')

    class Meta:
        db_table = 'todo'

