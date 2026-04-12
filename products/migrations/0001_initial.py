
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('image_url', models.URLField(blank=True, verbose_name='Image URL')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('stock', models.IntegerField(default=0, verbose_name='Stock')),
                ('is_combo', models.BooleanField(default=False, verbose_name='Is Combo')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ComboDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantity')),
                ('combo_parent', models.ForeignKey(limit_choices_to={'is_combo': True}, on_delete=django.db.models.deletion.CASCADE, related_name='combo_details', to='products.product')),
                ('product_child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_in_combos', to='products.product')),
            ],
            options={
                'verbose_name': 'Combo Detail',
                'verbose_name_plural': 'Combo Details',
                'unique_together': {('combo_parent', 'product_child')},
            },
        ),
    ]