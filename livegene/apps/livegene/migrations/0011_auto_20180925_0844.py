# Generated by Django 2.1.1 on 2018-09-25 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livegene', '0010_auto_20180924_1926'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='samplingdocumenttype',
            options={'ordering': ('short_name', 'long_name')},
        ),
    ]