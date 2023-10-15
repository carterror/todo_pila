from django.db import models
from django.db.models import (
    CharField, TextField, ImageField, ForeignKey, BooleanField, DateTimeField
)
from django.contrib.auth.models import User


# Create your models here.
class Todo(models.Model):
    title = CharField(max_length=50, null=False, blank=False, default="")
    description = TextField(max_length=300, null=True, blank=True)
    imagen = ImageField(upload_to='to_do', null=True)
    user = ForeignKey(User, on_delete=models.CASCADE, editable=False)
    status = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"
        ordering = ("updated", "created", "title", "status")

    def __str__(self):
        return self.title
