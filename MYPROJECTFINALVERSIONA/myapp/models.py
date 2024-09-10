from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique constraint to prevent duplicate names
    slug = models.SlugField(max_length=150, unique=True, blank=True)  # Auto-generated slug for SEO-friendly URLs
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)  # Allow blank descriptions
    img = models.ImageField(upload_to='products/', default='products/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the product was created
    updated_at = models.DateTimeField(auto_now=True)  # Track when the product was last updated
    is_active = models.BooleanField(default=True)  # Enable/disable products

    class Meta:
        ordering = ['-created_at']  # Order products by the latest created first
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the product name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # Provide a URL for the product detail page
        return reverse('product_detail', kwargs={'pk': self.pk})
