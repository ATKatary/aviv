# Generated by Django 5.0.7 on 2024-07-16 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0003_alter_event_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='trigger',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
