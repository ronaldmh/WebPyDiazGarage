# Generated by Django 4.2 on 2023-05-12 01:21

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id_car', models.AutoField(primary_key=True, serialize=False)),
                ('license', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=100)),
                ('serieNumber', models.CharField(max_length=100)),
                ('vin', models.CharField(max_length=100)),
                ('engine', models.CharField(max_length=100)),
                ('oil', models.CharField(max_length=100)),
                ('traction', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=250)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id_client', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id_service', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('mechanic', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=250)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('services', multiselectfield.db.fields.MultiSelectField(choices=[('TYRES', 'Tyres'), ('SUSPENSION', 'Suspension'), ('BREAKS', 'Breaks'), ('OIL', 'Oil'), ('PAINT', 'Paint'), ('BODYWORK', 'Bodywork'), ('ENGINE', 'Engine'), ('FAN', 'Fan'), ('ELECTRIC', 'Electric'), ('SCANNER', 'Scanner'), ('WASH', 'Wash'), ('GENERAL_INSPECTION', 'General Inspection'), ('MUFFLE', 'Muffle'), ('OTHER', 'Other')], max_length=107, verbose_name='Services provided')),
                ('id_car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.car')),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='id_client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client'),
        ),
    ]
