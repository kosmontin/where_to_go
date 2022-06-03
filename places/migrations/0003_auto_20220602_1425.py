# Generated by Django 3.2.13 on 2022-06-02 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20220601_1435'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name': 'Фотография', 'verbose_name_plural': 'Фотографии мест'},
        ),
        migrations.AlterField(
            model_name='photo',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place_images', to='places.place'),
        ),
    ]