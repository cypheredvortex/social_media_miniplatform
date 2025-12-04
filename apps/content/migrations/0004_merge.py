from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_populate_content_ptr'),
        ('content', '0002_populate_content_ptr'),
        ('content', '0003_populate_content_fk'),
    ]

    operations = [
        # This is an empty merge migration to unify the multiple leaf nodes
    ]
