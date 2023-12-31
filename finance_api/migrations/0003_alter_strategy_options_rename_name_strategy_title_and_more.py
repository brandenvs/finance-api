# Generated by Django 5.0 on 2023-12-31 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_api', '0002_strategy_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='strategy',
            options={'ordering': ['pinned']},
        ),
        migrations.RenameField(
            model_name='strategy',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='strategy',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]
