# Generated by Django 5.0.6 on 2024-10-07 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MindMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_keyword', models.CharField(max_length=100)),
                ('sub_keywords', models.JSONField(default=list)),
            ],
        ),
    ]
