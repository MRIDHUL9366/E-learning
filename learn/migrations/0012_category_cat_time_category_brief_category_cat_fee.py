# Generated by Django 5.0.7 on 2024-10-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0011_alter_exam_register_ex_reg_cou'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='Cat_time',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='brief',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='cat_fee',
            field=models.IntegerField(null=True),
        ),
    ]