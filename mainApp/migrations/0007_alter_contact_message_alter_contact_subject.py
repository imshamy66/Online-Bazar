# Generated by Django 4.0.4 on 2023-04-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_alter_contact_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(max_length=50),
        ),
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.TextField(max_length=50),
        ),
    ]
