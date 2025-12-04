from django.db import migrations

def forward_populate(apps, schema_editor):
    Content = apps.get_model('content', 'Content')
    Post = apps.get_model('post', 'Post')

    for post in Post.objects.all():
        content = Content.objects.create(
            text=getattr(post, 'text', '') or '',
            is_edited=getattr(post, 'is_edited', False),
            status=getattr(post, 'status', None) or 'ACTIVE'
        )
        # set FK to new content
        post.content_id = content.id
        post.save()

def reverse_populate(apps, schema_editor):
    # No reverse implemented
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
        ('post', '0002_add_content_fk'),
    ]

    operations = [
        migrations.RunPython(forward_populate, reverse_populate),
    ]
