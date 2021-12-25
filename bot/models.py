from django.db import models

# Create your models here.
class TodoItem(models.Model):
    todo_text = models.CharField(max_length=200)
    chat_id = models.CharField(max_length=100)