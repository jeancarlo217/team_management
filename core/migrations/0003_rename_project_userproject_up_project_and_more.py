# Generated by Django 5.1.3 on 2024-11-22 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_project_description_alter_project_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userproject',
            old_name='project',
            new_name='up_project',
        ),
        migrations.RenameField(
            model_name='userproject',
            old_name='user',
            new_name='up_user',
        ),
    ]