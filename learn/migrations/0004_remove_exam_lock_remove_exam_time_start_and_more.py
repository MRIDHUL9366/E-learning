# Generated by Django 5.0.7 on 2024-09-20 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0003_remove_exam_register_lock_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='Lock',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='Time_start',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='Time_stop',
        ),
        migrations.AddField(
            model_name='exam_register',
            name='Lock',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='exam_register',
            name='Time_start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='exam_register',
            name='Time_stop',
            field=models.DateTimeField(null=True),
        ),
    ]
