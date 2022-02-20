# Generated by Django 4.0.2 on 2022-02-18 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szalonebembeny', '0003_alter_order_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(choices=[(3, 'Wysłane'), (1, 'Zamówione'), (4, 'Odebrane'), (2, 'Opłacone')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='score',
            field=models.DecimalField(decimal_places=1, default=5.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='product',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]