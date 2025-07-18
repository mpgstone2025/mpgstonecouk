# Generated by Django 4.1.7 on 2025-07-14 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_aboutus_mission_image_aboutus_mission_image_alt_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCatalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('thumbnail', models.ImageField(upload_to='catalogue_thumbnails/')),
                ('pdf_file', models.FileField(upload_to='catalogue_pdfs/')),
            ],
        ),
    ]
