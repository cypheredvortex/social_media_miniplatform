from django.db import migrations

def forward_populate(apps, schema_editor):
    # Get historical models via apps.get_model
    Content = apps.get_model('content', 'Content')
    Post = apps.get_model('post', 'Post')

    # Create a Content instance for each existing Post and attach pointer
    for post in Post.objects.all():
        content = Content.objects.create(
            text=getattr(post, 'text', '') or '',
            is_edited=getattr(post, 'is_edited', False),
            status=getattr(post, 'status', None) or 'ACTIVE'
        )
        # Assign pointer field (will be present once schema migration runs)
        # Use content.id as the pointer value
        setattr(post, 'content_ptr_id', content.id)
        post.save()

def reverse_populate(apps, schema_editor):
    # No reverse operation implemented
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward_populate, reverse_populate),
    ]
