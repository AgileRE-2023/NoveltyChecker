# Generated by Django 4.2.4 on 2023-12-04 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='feedback_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
