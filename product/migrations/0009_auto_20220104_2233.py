# Generated by Django 3.1.7 on 2022-01-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20220104_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sizeandquantity',
            name='size',
            field=models.CharField(choices=[('32', '32'), ('34', '34'), ('36', '36'), ('38', '38'), ('40', '40'), ('short', 'S'), ('medium', 'M'), ('large', 'L'), ('extra large', 'XL'), ('extra x large', 'XXL')], max_length=30),
        ),
    ]
