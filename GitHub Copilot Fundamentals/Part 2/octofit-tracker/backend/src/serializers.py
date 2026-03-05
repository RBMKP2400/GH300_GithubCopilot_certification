from rest_framework import serializers
from .models import OctoFitUser, Team, Activity, Leaderboard, Workout


class OctoFitUserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()

    class Meta:
        model = OctoFitUser
        fields = ['_id', 'id', 'username', 'email', 'age', 'weight', 'height']

    def get__id(self, obj):
        return str(obj.pk)


class TeamSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    members = OctoFitUserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['_id', 'id', 'name', 'members']

    def get__id(self, obj):
        return str(obj.pk)


class ActivitySerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    user = OctoFitUserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['_id', 'id', 'user', 'activity_type', 'duration', 'date']

    def get__id(self, obj):
        return str(obj.pk)


class LeaderboardSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    user = OctoFitUserSerializer(read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['_id', 'id', 'user', 'score']

    def get__id(self, obj):
        return str(obj.pk)


class WorkoutSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['_id', 'id', 'name', 'description', 'exercises']

    def get__id(self, obj):
        return str(obj.pk)
