from django import forms

from .models import Note, SubTask, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "deadline",
            "status",
            "priority",
            "category",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["title", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={"class": "form-control", "rows": 3})}
