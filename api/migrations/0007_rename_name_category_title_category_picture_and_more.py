# Generated by Django 5.0.6 on 2024-05-25 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_order_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='category',
            name='picture',
            field=models.ImageField(blank=True, upload_to='categories_pictures/'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='product_pictures/'),
        ),
    ]
