# Generated by Django 4.0.4 on 2022-11-18 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0002_remove_proceeding_participants_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResolutionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resolution_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='resolution',
            name='resolution_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='resolution',
            name='result',
            field=models.BooleanField(default=True),
        ),
    ]
