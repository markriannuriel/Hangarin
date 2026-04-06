import os
from datetime import timedelta

import requests
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import NoteForm, SubTaskForm, TaskForm
from .models import Note, SubTask, Task


class TaskListView(generic.ListView):
    model = Task
    context_object_name = "tasks"
    paginate_by = 20
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        status = self.request.GET.get("status", "all")

        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)

        if status and status != "all":
            qs = qs.filter(status=status)

        return qs.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        all_tasks = Task.objects.all()

        status = self.request.GET.get("status", "all")

        context["q"] = self.request.GET.get("q", "")
        context["status"] = status
        context["status_choices"] = ["all", "Pending", "In Progress", "Completed"]

        context["total_tasks"] = all_tasks.count()
        context["pending_count"] = all_tasks.filter(status="Pending").count()
        context["in_progress_count"] = all_tasks.filter(status="In Progress").count()
        context["completed_count"] = all_tasks.filter(status="Completed").count()

        context["due_soon_tasks"] = (
            all_tasks
            .filter(deadline__gte=now, deadline__lte=now + timedelta(days=2))
            .exclude(status="Completed")
            .order_by("deadline")[:5]
        )
        context["overdue_tasks"] = (
            all_tasks.filter(deadline__lt=now).exclude(status="Completed").order_by("deadline")[:5]
        )
        context["recent_tasks"] = all_tasks.order_by("-created_at")[:5]

        weather_city = self.request.GET.get("weather_city", "Manila")
        context["weather_city"] = weather_city
        context["weather_data"] = self.get_weather_data(weather_city)
        return context

    def get_weather_data(self, city="Manila"):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return {
                "error": "OpenWeather API key not configured. Set OPENWEATHER_API_KEY in your environment.",
            }

        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            forecast_items = []
            for item in data.get("list", [])[:6]:
                forecast_items.append({
                    "time": item["dt_txt"],
                    "temp": round(item["main"]["temp"]),
                    "description": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"],
                })

            return {
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "current": forecast_items[0] if forecast_items else {},
                "forecast": forecast_items,
            }
        except requests.exceptions.RequestException as exc:
            return {
                "error": "Unable to fetch weather data. Please check your network or API key.",
                "details": str(exc),
            }
        except (KeyError, IndexError):
            return {
                "error": f"No weather data found for '{city}'.",
            }


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task_list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name_suffix = "_form"

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task_list")


class SubTaskCreateView(generic.CreateView):
    model = SubTask
    form_class = SubTaskForm

    def dispatch(self, request, *args, **kwargs):
        self.task = Task.objects.get(pk=kwargs["task_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.parent_task = self.task
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.task.pk})


class NoteCreateView(generic.CreateView):
    model = Note
    form_class = NoteForm

    def dispatch(self, request, *args, **kwargs):
        self.task = Task.objects.get(pk=kwargs["task_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.task = self.task
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.task.pk})


def manifest(request):
    """Serve PWA manifest.json"""
    manifest_data = {
        "name": "Hangarin Task Manager",
        "short_name": "Hangarin",
        "description": "A Progressive Web App for task management and organization",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait-primary",
        "theme_color": "#1b4332",
        "background_color": "#fafaf7",
        "categories": ["productivity"],
        "icons": [
            {
                "src": "/static/img/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/img/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/img/icon-512x512-maskable.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable"
            }
        ]
    }
    return JsonResponse(manifest_data)
