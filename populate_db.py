import os
import django
import random
from faker import Faker

# ---------- Django Setup ----------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Participant


def populate_db():
    fake = Faker()

    # ---------- Categories ----------
    category_choices = [
        'Workshop', 'Conference', 'Meetup', 'Seminar', 'Bootcamp', 'Webinar'
    ]

    categories = []
    for choice in category_choices:
        category, created = Category.objects.get_or_create(
            name=choice.lower(),
            defaults={'description': fake.sentence()}
        )
        categories.append(category)
    print(f"Created {len(categories)} categories.")

    # ---------- Events ----------
    events = []
    for _ in range(10):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            date=fake.date_this_year(),
            location=fake.city(),
            category=random.choice(categories),
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # ---------- Participants ----------
    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email(),
        )
        # এক বা একাধিক event assign করা
        participant.events.set(random.sample(events, k=random.randint(1, 3)))
        participants.append(participant)
    print(f"Created {len(participants)} participants.")

    print("✅ Database populated successfully!")


if __name__ == "__main__":
    populate_db()
