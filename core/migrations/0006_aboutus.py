# Generated by Django 4.1.7 on 2025-07-14 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='about/')),
                ('image_1_alt', models.CharField(blank=True, help_text='Alt text for image 1', max_length=255)),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='about/')),
                ('image_2_alt', models.CharField(blank=True, help_text='Alt text for image 2', max_length=255)),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='about/')),
                ('image_3_alt', models.CharField(blank=True, help_text='Alt text for image 3', max_length=255)),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='about/')),
                ('image_4_alt', models.CharField(blank=True, help_text='Alt text for image 4', max_length=255)),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='about/')),
                ('image_5_alt', models.CharField(blank=True, help_text='Alt text for image 5', max_length=255)),
                ('mission', models.TextField()),
                ('vision', models.TextField()),
                ('values', models.TextField()),
                ('philosophy', models.TextField()),
            ],
        ),
    ]
