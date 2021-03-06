# Generated by Django 3.1.7 on 2022-01-04 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20220104_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_category',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.maincategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_category',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.subcategory'),
        ),
    ]
