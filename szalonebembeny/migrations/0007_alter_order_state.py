# Generated by Django 4.0.2 on 2022-02-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szalonebembeny', '0006_alter_product_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(choices=[(1, 'Zamówione'), (3, 'Wysłane'), (2, 'Opłacone'), (4, 'Odebrane')], default=1),
        ),
    ]