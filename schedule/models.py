from django.db import models


class Division(models.Model):
    name = models.CharField(max_length=50)
    max_overs = models.IntegerField(default=50)
    match_duration = models.FloatField(default=3)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ground(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='schedule_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='schedule_team2')
    ground = models.ForeignKey(Ground, on_delete=models.CASCADE)
    schedule_time = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return "%s , %s" % (self.team1.name, self.team2.name)
