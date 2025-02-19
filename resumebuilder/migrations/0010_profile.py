# Generated by Django 5.1.3 on 2024-12-09 15:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumebuilder', '0009_delete_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiences', models.ManyToManyField(blank=True, to='resumebuilder.experience')),
                ('jobs', models.ManyToManyField(blank=True, to='resumebuilder.job')),
                ('skills', models.ManyToManyField(blank=True, to='resumebuilder.skill')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
