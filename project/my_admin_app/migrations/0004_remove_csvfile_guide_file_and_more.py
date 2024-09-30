# Generated by Django 5.0.1 on 2024-09-30 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("my_admin_app", "0003_remove_csvfile_file_csvfile_guide_file_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="csvfile",
            name="guide_file",
        ),
        migrations.RemoveField(
            model_name="csvfile",
            name="student_file",
        ),
        migrations.AddField(
            model_name="csvfile",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="csvs/"),
        ),
    ]
