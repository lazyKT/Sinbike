# Generated by Django 3.2.5 on 2021-07-13 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sinbike_Customers', '0006_auto_20210712_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_point', models.CharField(max_length=16)),
                ('end_point', models.CharField(max_length=16)),
                ('distance', models.FloatField(default=0.0)),
                ('fare', models.FloatField(default=0.0)),
                ('promo', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sinbike_Customers.customer')),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
    ]
