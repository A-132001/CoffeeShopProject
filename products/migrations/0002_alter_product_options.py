# Generated by Django 4.1.7 on 2023-03-20 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-publish_date']},
        ),
    ]
