from django.db import models


class OctoFitUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    members = models.ManyToManyField(OctoFitUser, blank=True)

    class Meta:
        db_table = "teams"

    def __str__(self):
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(OctoFitUser, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    date = models.DateField()

    class Meta:
        db_table = "activities"

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} ({self.duration} min)"


class Leaderboard(models.Model):
    user = models.ForeignKey(OctoFitUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = "leaderboard"

    def __str__(self):
        return f"{self.user.username}: {self.score}"


class Workout(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    exercises = models.TextField(help_text="Comma-separated list of exercises")

    class Meta:
        db_table = "workouts"

    def __str__(self):
        return self.name
