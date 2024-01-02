from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caught_fish', '0002_alter_caught_fish_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caught_fish',
            name='main_fish_accuracy',
        ),
        migrations.RemoveField(
            model_name='caught_fish',
            name='main_fish_id',
        ),
        migrations.RemoveField(
            model_name='caught_fish',
            name='sub1_fish_accuracy',
        ),
        migrations.RemoveField(
            model_name='caught_fish',
            name='sub1_fish_id',
        ),
        migrations.RemoveField(
            model_name='caught_fish',
            name='sub2_fish_accuracy',
        ),
        migrations.RemoveField(
            model_name='caught_fish',
            name='sub2_fish_id',
        ),
        migrations.AddField(
            model_name='caught_fish',
            name='description',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='caught_fish',
            name='fish_name',
        ),
        migrations.AlterField(
            model_name='caught_fish',
            name='image_url',
            field=models.CharField(max_length=225, null=True),
        ),
