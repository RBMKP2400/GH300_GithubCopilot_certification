"""Management command: Populate the octofit_db database with test data"""
import datetime
from django.core.management.base import BaseCommand
from src.models import OctoFitUser, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🗑️  Deleting existing data...')
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Team.objects.all().delete()
        OctoFitUser.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write('🦸 Creating superhero users...')
        users_data = [
            # Team Marvel
            {'username': 'ironman', 'email': 'tony@starkindustries.com', 'password': 'ironman123', 'age': 45, 'weight': 95.0, 'height': 185.0},
            {'username': 'spiderman', 'email': 'peter@dailybugle.com', 'password': 'spidey123', 'age': 19, 'weight': 75.0, 'height': 178.0},
            {'username': 'blackwidow', 'email': 'natasha@shield.com', 'password': 'natasha123', 'age': 35, 'weight': 60.0, 'height': 170.0},
            {'username': 'thor', 'email': 'thor@asgard.com', 'password': 'mjolnir123', 'age': 1500, 'weight': 290.0, 'height': 198.0},
            # Team DC
            {'username': 'batman', 'email': 'bruce@wayneenterprises.com', 'password': 'batman123', 'age': 38, 'weight': 95.0, 'height': 188.0},
            {'username': 'superman', 'email': 'clark@dailyplanet.com', 'password': 'superman123', 'age': 33, 'weight': 107.0, 'height': 191.0},
            {'username': 'wonderwoman', 'email': 'diana@themyscira.com', 'password': 'amazon123', 'age': 800, 'weight': 74.0, 'height': 183.0},
            {'username': 'theflash', 'email': 'barry@ccpd.com', 'password': 'flash123', 'age': 28, 'weight': 79.0, 'height': 180.0},
        ]

        users = {}
        for data in users_data:
            user = OctoFitUser.objects.create(**data)
            users[data['username']] = user
            self.stdout.write(f'  ✅ Created user: {data["username"]}')

        self.stdout.write('🦸‍♂️ Creating teams...')
        team_marvel = Team.objects.create(name='Team Marvel')
        team_marvel.members.set([users['ironman'], users['spiderman'], users['blackwidow'], users['thor']])
        team_marvel.save()
        self.stdout.write('  ✅ Created Team Marvel')

        team_dc = Team.objects.create(name='Team DC')
        team_dc.members.set([users['batman'], users['superman'], users['wonderwoman'], users['theflash']])
        team_dc.save()
        self.stdout.write('  ✅ Created Team DC')

        self.stdout.write('🏋️ Creating activities...')
        activities_data = [
            {'user': users['ironman'], 'activity_type': 'Strength Training', 'duration': 60, 'date': datetime.date(2024, 1, 15)},
            {'user': users['spiderman'], 'activity_type': 'Parkour', 'duration': 45, 'date': datetime.date(2024, 1, 16)},
            {'user': users['blackwidow'], 'activity_type': 'Martial Arts', 'duration': 90, 'date': datetime.date(2024, 1, 17)},
            {'user': users['thor'], 'activity_type': 'Hammer Throws', 'duration': 30, 'date': datetime.date(2024, 1, 18)},
            {'user': users['batman'], 'activity_type': 'Combat Training', 'duration': 120, 'date': datetime.date(2024, 1, 15)},
            {'user': users['superman'], 'activity_type': 'Flying', 'duration': 50, 'date': datetime.date(2024, 1, 16)},
            {'user': users['wonderwoman'], 'activity_type': 'Sparring', 'duration': 75, 'date': datetime.date(2024, 1, 17)},
            {'user': users['theflash'], 'activity_type': 'Speed Running', 'duration': 20, 'date': datetime.date(2024, 1, 18)},
        ]

        for data in activities_data:
            Activity.objects.create(**data)
        self.stdout.write(f'  ✅ Created {len(activities_data)} activities')

        self.stdout.write('🏆 Creating leaderboard entries...')
        leaderboard_data = [
            {'user': users['ironman'], 'score': 950},
            {'user': users['thor'], 'score': 1200},
            {'user': users['spiderman'], 'score': 820},
            {'user': users['blackwidow'], 'score': 880},
            {'user': users['batman'], 'score': 1100},
            {'user': users['superman'], 'score': 1300},
            {'user': users['wonderwoman'], 'score': 1050},
            {'user': users['theflash'], 'score': 990},
        ]

        for data in leaderboard_data:
            Leaderboard.objects.create(**data)
        self.stdout.write(f'  ✅ Created {len(leaderboard_data)} leaderboard entries')

        self.stdout.write('💪 Creating workouts...')
        workouts_data = [
            {
                'name': 'Avengers Assemble',
                'description': 'High intensity full body workout inspired by the Avengers',
                'exercises': 'Iron Press,Spider Crawls,Black Widow Kicks,Thor Squats',
            },
            {
                'name': 'Justice League Circuit',
                'description': 'Endurance circuit inspired by the Justice League',
                'exercises': 'Batman Burpees,Superman Planks,Wonder Woman Lunges,Flash Sprints',
            },
            {
                'name': 'Super Strength Builder',
                'description': 'Build superhero-level strength',
                'exercises': 'Deadlifts,Bench Press,Overhead Press,Pull-ups,Barbell Squats',
            },
            {
                'name': 'Cardio Blitz',
                'description': 'Speed and endurance like The Flash',
                'exercises': 'Interval Sprints,Jump Rope,Box Jumps,High Knees,Mountain Climbers',
            },
        ]

        for data in workouts_data:
            Workout.objects.create(**data)
        self.stdout.write(f'  ✅ Created {len(workouts_data)} workouts')

        self.stdout.write(self.style.SUCCESS('🎉 Database populated successfully!'))
