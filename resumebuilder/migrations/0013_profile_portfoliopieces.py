# Generated by Django 5.1.3 on 2024-12-10 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0012_portfoliopiece'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='portfoliopieces',
            field=models.ManyToManyField(blank=True, related_name='profile', to='resumebuilder.portfoliopiece'),
        ),
    ]
