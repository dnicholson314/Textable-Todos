# Generated by Django 5.0.4 on 2024-09-04 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0008_alter_config_discord_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='discord_username',
            field=models.CharField(blank=True, default='', max_length=200, unique=True),
        ),
    ]
