from django.core.management.base import BaseCommand
from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activity.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Drop existing indexes for all collections
        db.users.drop_indexes()
        db.teams.drop_indexes()
        db.activity.drop_indexes()
        db.leaderboard.drop_indexes()
        db.workouts.drop_indexes()

        # Populate users
        users = [
            {'_id': ObjectId(), 'email': 'john.doe@example.com', 'name': 'John Doe', 'password': 'password123'},
            {'_id': ObjectId(), 'email': 'jane.smith@example.com', 'name': 'Jane Smith', 'password': 'password123'},
        ]
        db.users.insert_many(users)

        # Populate teams
        teams = [
            {'_id': ObjectId(), 'name': 'Team Alpha', 'members': ['John Doe', 'Jane Smith']},
            {'_id': ObjectId(), 'name': 'Team Beta', 'members': ['Alice', 'Bob']},
        ]
        db.teams.insert_many(teams)

        # Populate activities
        activities = [
            {'_id': ObjectId(), 'user_email': 'john.doe@example.com', 'type': 'Running', 'duration': 30},
            {'_id': ObjectId(), 'user_email': 'jane.smith@example.com', 'type': 'Cycling', 'duration': 45},
        ]
        db.activity.insert_many(activities)

        # Populate leaderboard
        leaderboard = [
            {'_id': ObjectId(), 'team_name': 'Team Alpha', 'score': 100},
            {'_id': ObjectId(), 'team_name': 'Team Beta', 'score': 80},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Populate workouts
        workouts = [
            {'_id': ObjectId(), 'name': 'Push-ups', 'description': 'Do 20 push-ups'},
            {'_id': ObjectId(), 'name': 'Squats', 'description': 'Do 30 squats'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data'))
