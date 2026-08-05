from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('title', models.CharField(max_length=300, verbose_name='Slide Caption / Title')),
                ('image', models.ImageField(upload_to='home/slides/', verbose_name='Slide Photo / Image')),
                ('link', models.CharField(blank=True, max_length=500, verbose_name='Target Link (Optional)')),
                ('is_published', models.BooleanField(default=True, verbose_name='Active / Published')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Display Order')),
            ],
            options={
                'verbose_name': 'Hero Slideshow Photo',
                'verbose_name_plural': 'Hero Slideshow Photos',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
