from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from tasks.models import Task, SubTask, Note, Priority, Category
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Seed fake data'

    def handle(self, *args, **kwargs):
        # Ensure we have some priorities and categories to relate tasks to
        priority_names = ["Low", "Medium", "High"]
        priorities = [Priority.objects.get_or_create(name=name)[0] for name in priority_names]

        category_names = ["Work", "Personal", "Errands"]
        categories = [Category.objects.get_or_create(name=name)[0] for name in category_names]

        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                priority=random.choice(priorities),
                category=random.choice(categories),
            )

            # Add subtasks
            for _ in range(2):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                )

            # Add notes
            Note.objects.create(task=task, content=fake.paragraph(nb_sentences=2))

        self.stdout.write(self.style.SUCCESS('Fake data seeded successfully!'))