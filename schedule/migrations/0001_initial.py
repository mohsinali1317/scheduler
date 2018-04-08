# Generated by Django 2.0 on 2018-04-07 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('max_overs', models.IntegerField(default=50)),
                ('match_duration', models.FloatField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Ground',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_time', models.DateTimeField()),
                ('ground', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Ground')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Division')),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_team1', to='schedule.Team'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_team2', to='schedule.Team'),
        ),
    ]
