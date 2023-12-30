# Generated by Django 5.0 on 2023-12-27 19:34

import django.db.models.deletion
import media.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to=media.models.PathAndRename('media_files/'))),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=media.models.PathAndRename('media_files/thumbnails/'))),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file_type', models.CharField(blank=True, editable=False, max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]