from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def __str__(self):
        return self.title
    

class Media(models.Model):
    product = models.ForeignKey(Product, related_name='media', on_delete=models.CASCADE)
    image = models.FileField(upload_to='product_images', null=True, blank=True)
    is_top = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title
