from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_add_content_fk'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.ForeignKey(on_delete=models.CASCADE, to='content.content', related_name='posts'),
        ),
    ]
