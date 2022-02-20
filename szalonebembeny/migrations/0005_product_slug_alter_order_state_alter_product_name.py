# Generated by Django 4.0.2 on 2022-02-20 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szalonebembeny', '0004_alter_order_state_alter_product_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='name', max_length=64, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(choices=[(4, 'Odebrane'), (2, 'Opłacone'), (1, 'Zamówione'), (3, 'Wysłane')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
