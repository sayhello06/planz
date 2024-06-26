from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "TodoListApp_db"