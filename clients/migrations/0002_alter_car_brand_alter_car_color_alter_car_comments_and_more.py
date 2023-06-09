# Generated by Django 4.2 on 2023-05-12 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='color',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='comments',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='license',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='oil',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='serieNumber',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='traction',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='version',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='vin',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
