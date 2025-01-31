# Generated by Django 3.1.4 on 2021-04-22 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journey', models.CharField(max_length=225)),
                ('DateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('icon', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('author', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Domino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=255)),
                ('body', models.TextField(blank=True)),
                ('DateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('DateLastEditted', models.DateTimeField(default=django.utils.timezone.now)),
                ('DateCompleted', models.DateTimeField(blank=True, null=True)),
                ('DatePinned', models.DateTimeField(blank=True, null=True)),
                ('isPinned', models.BooleanField(default=False)),
                ('isCompleted', models.BooleanField(default=False)),
                ('timeset', models.BooleanField(default=False)),
                ('assignedJourney', models.ManyToManyField(blank=True, to='journal.Collection')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parentId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='journal.domino')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='domino', max_length=255)),
                ('icon', models.CharField(default='circle', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TimeBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeset', models.DateTimeField()),
                ('description', models.CharField(blank=True, max_length=255)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('domino', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='journal.domino')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=225)),
                ('content', models.TextField()),
                ('DateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('domino', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='journal.domino')),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('checked', models.BooleanField(default=False)),
                ('domino', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='journal.domino')),
            ],
        ),
    ]
