# Generated by Django 4.0.2 on 2022-02-25 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szalonebembeny', '0010_alter_category_description_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imgpath',
            field=models.CharField(default='Brak zdjęcia', max_length=64),
        ),
        migrations.AlterField(
            model_name='order',
            name='deliver_method',
            field=models.CharField(choices=[('DPD', 'Kurier DPD'), ('paczkomat', 'Paczkomat Inpost'), ('poczta', 'Poczta Polska')], max_length=32),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('BLIK', 'Płatność BLIK'), ('pobranie', 'Za pobraniem'), ('przelew', 'Przelew internetowy')], max_length=32),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(choices=[(2, 'Opłacone'), (4, 'Odebrane'), (3, 'Wysłane'), (1, 'Zamówione')], default=1),
        ),
    ]
