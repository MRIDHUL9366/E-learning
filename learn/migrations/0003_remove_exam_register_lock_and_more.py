# Generated by Django 5.0.7 on 2024-09-18 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_remove_exam_lock_remove_exam_time_start_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam_register',
            name='Lock',
        ),
        migrations.RemoveField(
            model_name='exam_register',
            name='Time_start',
        ),
        migrations.RemoveField(
            model_name='exam_register',
            name='Time_stop',
        ),
        migrations.AddField(
            model_name='exam',
            name='Lock',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='Time_start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='Time_stop',
            field=models.DateTimeField(null=True),
        ),
    ]