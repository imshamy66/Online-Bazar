# Generated by Django 4.0.4 on 2023-04-10 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_alter_contact_message_alter_contact_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.CharField(default='In Stock', max_length=30),
        ),
    ]
