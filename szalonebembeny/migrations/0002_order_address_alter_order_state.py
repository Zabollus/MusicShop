# Generated by Django 4.0.2 on 2022-02-18 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szalonebembeny', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(choices=[(1, 'Zamówione'), (3, 'Wysłane'), (2, 'Opłacone'), (4, 'Odebrane')]),
        ),
    ]
