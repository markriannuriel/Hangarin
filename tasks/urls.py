from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("tasks/new/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_edit"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),

    path(
        "tasks/<int:task_pk>/subtasks/add/",
        views.SubTaskCreateView.as_view(),
        name="subtask_add",
    ),
    path(
        "tasks/<int:task_pk>/notes/add/",
        views.NoteCreateView.as_view(),
        name="note_add",
    ),
]
