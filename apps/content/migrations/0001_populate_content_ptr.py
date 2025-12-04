from django.db import migrations

def forward_populate(apps, schema_editor):
    # Get historical models via apps.get_model
    Content = apps.get_model('content', 'Content')
    Post = apps.get_model('post', 'Post')

    # If using djongo/ObjectIdField, id creation will be handled by the ORM
    for post in Post.objects.all():
        # Create a Content instance using fields available on Post.
        # Adjust field mapping if your Post stores text under another name.
        content = Content.objects.create(
            text=getattr(post, 'text', '') or '',
            is_edited=getattr(post, 'is_edited', False),
            status=getattr(post, 'status', None) or 'ACTIVE'
        )
        # Set the multi-table inheritance pointer on Post (content_ptr_id)
        # The field name is 'content_ptr_id' because Django uses <base>_ptr for multi-table inheritance.
        # For djongo/ObjectIdField, this assignment should work; set the raw PK as produced by Content.
        post.content_ptr_id = content.id
        post.save()

def reverse_populate(apps, schema_editor):
    # Optional: reverse migration not implemented (noop) or remove created Content rows.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),  # adjust if different
        ('post', '0001_initial'),     # adjust if different
    ]

    operations = [
        migrations.RunPython(forward_populate, reverse_populate),
    ]