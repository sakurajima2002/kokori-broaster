from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    is_combo = models.BooleanField(default=False, verbose_name="Is Combo")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    @property
    def original_value(self):
        if not self.is_combo:
            return self.price
        return sum(detail.product_child.price * detail.quantity for detail in self.combo_details.all())

    @property
    def savings(self):
        if not self.is_combo:
            return 0
        return self.original_value - self.price



class ComboDetail(models.Model):
    combo_parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='combo_details', limit_choices_to={'is_combo': True})
    product_child = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='used_in_combos')
    quantity = models.IntegerField(default=1, verbose_name="Quantity")

    class Meta:
        verbose_name = "Combo Detail"
        verbose_name_plural = "Combo Details"
        unique_together = ('combo_parent', 'product_child')

    def __str__(self):
        return f"{self.combo_parent.name} - {self.product_child.name} x{self.quantity}"
