# Generated by Django 5.0.4 on 2024-07-25 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0006_alter_discordauthtoken_access_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='discord_id',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.DeleteModel(
            name='DiscordAuthToken',
        ),
    ]
