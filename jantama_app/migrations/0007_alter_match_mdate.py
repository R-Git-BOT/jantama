# Generated by Django 3.2 on 2021-05-10 04:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jantama_app', '0006_alter_match_mdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='mdate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='match date'),
        ),
    ]
