# Generated by Django 2.2.14 on 2021-07-27 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sinbike_Bikes', '0003_alter_bike_reserved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reserved_time',
            field=models.DateTimeField(),
        ),
    ]
