from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Users (superheroes)
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "marvel"},
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
        ]
        db.users.insert_many(users)
        db.users.create_index("email", unique=True)

        # Teams
        teams = [
            {"name": "marvel", "members": [u["email"] for u in users if u["team"] == "marvel"]},
            {"name": "dc", "members": [u["email"] for u in users if u["team"] == "dc"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user_email": "ironman@marvel.com", "activity": "Running", "duration": 30},
            {"user_email": "cap@marvel.com", "activity": "Cycling", "duration": 45},
            {"user_email": "spiderman@marvel.com", "activity": "Swimming", "duration": 25},
            {"user_email": "superman@dc.com", "activity": "Flying", "duration": 60},
            {"user_email": "batman@dc.com", "activity": "Martial Arts", "duration": 40},
            {"user_email": "wonderwoman@dc.com", "activity": "Weightlifting", "duration": 35},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"team": "marvel", "points": 100},
            {"team": "dc", "points": 120},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"name": "Hero HIIT", "suggested_for": ["marvel", "dc"]},
            {"name": "Power Yoga", "suggested_for": ["dc"]},
            {"name": "Web Sling", "suggested_for": ["marvel"]},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
