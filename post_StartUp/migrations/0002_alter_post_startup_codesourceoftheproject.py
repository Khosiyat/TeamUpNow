# Generated by Django 4.2.3 on 2023-07-29 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_StartUp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post_startup',
            name='codeSourceOfTheProject',
            field=models.URLField(blank=True, default='founderinstitute.com', null=True, verbose_name='founderinstitute.com'),
        ),
    ]
