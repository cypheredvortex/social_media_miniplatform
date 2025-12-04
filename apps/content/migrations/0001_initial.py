from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('DELETED', 'Deleted'), ('FLAGGED', 'Flagged')], default='ACTIVE', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
