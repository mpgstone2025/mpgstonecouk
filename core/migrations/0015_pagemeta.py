# Generated by Django 4.1.7 on 2025-07-15 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_homepagecontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(choices=[('products', 'Products'), ('about', 'About Us'), ('contact', 'Contact Us'), ('terms', 'Terms & Conditions'), ('privacy', 'Privacy Policy'), ('catalogue', 'Product Catalogue'), ('category', 'Category'), ('blogs', 'Blogs')], max_length=50, unique=True)),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('meta_image', models.ImageField(blank=True, null=True, upload_to='pages/meta_images/')),
                ('og_title', models.CharField(blank=True, max_length=255, null=True)),
                ('og_description', models.TextField(blank=True, null=True)),
                ('twitter_title', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_description', models.TextField(blank=True, null=True)),
                ('meta_keywords', models.TextField(blank=True, null=True)),
                ('canonical_url', models.URLField(blank=True, null=True)),
                ('robots_tag', models.CharField(default='INDEX, FOLLOW, MAX-IMAGE-PREVIEW:LARGE, MAX-SNIPPET:-1, MAX-VIDEO-PREVIEW:-1', max_length=255)),
                ('publisher', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
