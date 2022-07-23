# Generated by Django 4.0.6 on 2022-07-23 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Background_color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'background_colors',
            },
        ),
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('public', models.BooleanField()),
            ],
            options={
                'db_table': 'buckets',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=1000)),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'fonts',
            },
        ),
        migrations.CreateModel(
            name='Font_color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'font_colors',
            },
        ),
        migrations.CreateModel(
            name='Font_size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField()),
            ],
            options={
                'db_table': 'font_sizes',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=5000)),
                ('x_axis', models.IntegerField()),
                ('y_axis', models.IntegerField()),
                ('background_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buckets.background_color')),
                ('bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buckets.bucket')),
                ('font', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buckets.font')),
                ('font_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buckets.font_color')),
                ('font_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buckets.font_size')),
            ],
            options={
                'db_table': 'papers',
            },
        ),
        migrations.CreateModel(
            name='Paper_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=2000)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buckets.paper')),
            ],
            options={
                'db_table': 'paper_images',
            },
        ),
    ]