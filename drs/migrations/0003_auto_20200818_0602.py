# Generated by Django 3.0.8 on 2020-08-18 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drs', '0002_auto_20200818_0523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='type_form',
        ),
        migrations.AddField(
            model_name='form',
            name='form_type',
            field=models.CharField(blank=True, choices=[('rp', 'Report'), ('le', 'Leave Early'), ('lo', 'Leave Out'), ('il', 'In Late')], default='rp', help_text='Form type', max_length=2),
        ),
    ]
