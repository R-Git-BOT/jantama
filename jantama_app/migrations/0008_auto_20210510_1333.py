# Generated by Django 3.2 on 2021-05-10 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jantama_app', '0007_alter_match_mdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='dan',
            field=models.CharField(default='shin1', max_length=10, verbose_name='now danni'),
        ),
        migrations.AlterField(
            model_name='match',
            name='rank',
            field=models.IntegerField(verbose_name='match rank'),
        ),
    ]
