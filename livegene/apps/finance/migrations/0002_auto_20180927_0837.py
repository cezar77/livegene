# Generated by Django 2.1.1 on 2018-09-27 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenditure',
            name='report_date',
            field=models.DateTimeField(),
        ),
    ]
