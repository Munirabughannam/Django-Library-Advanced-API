# Generated by Django 4.1.2 on 2023-02-16 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_checkedoutbooks_reserved_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkedoutbooks',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.reservingbooks'),
        ),
        migrations.AlterField(
            model_name='checkedoutbooks',
            name='reserved_books',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.libraryinventory'),
        ),
    ]
