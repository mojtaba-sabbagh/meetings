# Generated by Django 4.0.4 on 2022-12-31 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0003_resolutiontype_resolution_resolution_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resolution',
            name='stockholder_type',
            field=models.CharField(choices=[('دانشجو', 'دانشجو'), ('کارکنان', 'کارکنان')], max_length=64),
        ),
    ]
