# Generated by Django 4.1 on 2022-10-08 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprava', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pojistenec',
            new_name='Uivatel',
        ),
        migrations.AlterModelOptions(
            name='uivatel',
            options={'verbose_name': 'Uživatel', 'verbose_name_plural': 'Uživatelé'},
        ),
    ]