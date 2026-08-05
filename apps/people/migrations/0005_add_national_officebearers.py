from django.db import migrations
from django.utils.text import slugify


def make_unique_slug(model, name):
    base_slug = slugify(name)
    slug = base_slug or 'office-bearer'
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}" if base_slug else f"office-bearer-{counter}"
        counter += 1
    return slug


def create_national_bearers(apps, schema_editor):
    OfficeBearer = apps.get_model('people', 'OfficeBearer')
    bearers = [
        {
            'name': 'Amit Sharma',
            'role': 'National President',
            'category': 'president',
            'state': '',
            'is_featured': True,
            'is_national': True,
            'order': 1,
        },
        {
            'name': 'Neha Kapoor',
            'role': 'National Secretary General',
            'category': 'secretary_general',
            'state': '',
            'is_featured': True,
            'is_national': True,
            'order': 2,
        },
        {
            'name': 'Ravi Joshi',
            'role': 'National Treasurer',
            'category': 'treasurer',
            'state': '',
            'is_featured': True,
            'is_national': True,
            'order': 3,
        },
        {
            'name': 'Priya Singh',
            'role': 'National Joint Secretary',
            'category': 'joint_secretary',
            'state': '',
            'is_featured': True,
            'is_national': True,
            'order': 4,
        },
    ]

    for bearer_data in bearers:
        bearer_data['slug'] = make_unique_slug(OfficeBearer, bearer_data['name'])
        OfficeBearer.objects.create(**bearer_data)


def remove_national_bearers(apps, schema_editor):
    OfficeBearer = apps.get_model('people', 'OfficeBearer')
    OfficeBearer.objects.filter(
        name__in=['Amit Sharma', 'Neha Kapoor', 'Ravi Joshi', 'Priya Singh'],
        is_national=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_officebearer_is_national'),
    ]

    operations = [
        migrations.RunPython(create_national_bearers, remove_national_bearers),
    ]
