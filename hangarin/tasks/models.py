from datetime import timedelta

from django.db import models
from django.utils import timezone


# BaseModel
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("In Progress", "In Progress"),
    ("Completed", "Completed"),
]

class Priority(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name

class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        if self.deadline and self.status != "Completed":
            return timezone.now() > self.deadline
        return False

    @property
    def due_status_badge(self):
        if self.status == "Completed":
            return "badge-completed"
        if self.is_overdue:
            return "badge-overdue"
        if self.deadline and timezone.now() + timedelta(days=1) >= self.deadline:
            return "badge-due-soon"
        return "badge-pending"

class SubTask(BaseModel):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return self.title

class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()

    def __str__(self):
        return f"Note for {self.task.title}"