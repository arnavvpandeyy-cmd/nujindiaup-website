from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsroom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsPostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='newsroom/news/gallery/', verbose_name='Image')),
                ('caption', models.CharField(blank=True, max_length=300, verbose_name='Caption')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('post', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='extra_images',
                    to='newsroom.newspost',
                    verbose_name='News Post'
                )),
            ],
            options={
                'verbose_name': 'News Post Image',
                'verbose_name_plural': 'News Post Images',
                'ordering': ['order'],
            },
        ),
    ]
