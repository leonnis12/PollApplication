# Generated by Django 3.1.3 on 2020-12-29 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Poll_app', '0002_auto_20201229_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
