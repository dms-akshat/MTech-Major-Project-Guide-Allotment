# Generated by Django 5.1 on 2024-09-30 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocate', '0003_student_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(default='1234567890', max_length=15),
        ),
    ]
