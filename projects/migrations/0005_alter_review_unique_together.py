# Generated by Django 4.0 on 2022-02-03 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_social_stack_over_flow'),
        ('projects', '0004_alter_project_owner'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('owner', 'project')},
        ),
    ]
