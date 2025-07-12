from django.db import migrations


def replace_nulls(apps, schema_editor):
    Place = apps.get_model('places', 'Place')
    Place.objects.filter(short_description__isnull=True).update(short_description='')
    Place.objects.filter(long_description__isnull=True).update(long_description='')


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0006_alter_place_title'),
    ]

    operations = [
        migrations.RunPython(replace_nulls),
    ]
