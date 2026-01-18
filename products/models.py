from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from colorfield.fields import ColorField

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    color = ColorField(default='#777777')
 
    class Meta:
        verbose_name_plural = "kategorie"
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
 
    def __str__(self):
        return self.name
 
class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    website = models.URLField(blank=True)
    def __str__(self):
        return self.name
 
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    sku = models.CharField(max_length=50, blank=True, null=True, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    discount = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(99),
        ],
        help_text="Discount (0–99)"
    )
    available = models.DecimalField(decimal_places=0, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # opcjonalnie: główny obraz
    main_image = models.ImageField(upload_to='products/main/', null=True, blank=True)
 
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['name']), models.Index(fields=['price'])]
 
    def short(self, limit=100):
        text = self.description
        return text if len(text) <= limit else text[:limit] + '...'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:200]
            unique = base
            i = 1
            # proste zapewnienie unikalności slug (możesz poprawić)
            while Product.objects.filter(slug=unique).exists():
                unique = f"{base}-{i}"
                i += 1
            self.slug = unique
        super().save(*args, **kwargs)
 
    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})
 
    def __str__(self):
        return self.name
 
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/')
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        ordering = ['order']
 
    def __str__(self):
        return f"Image for {self.product.name}"
 
class ProductVariant(models.Model):
    """
    Wariant produktu (np. kolor/rozmiar). Jeśli nie potrzebujesz wariantów, możesz pominąć.
    """
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)  # np. "Czerwony", "Rozmiar 3-5"
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    stock = models.PositiveIntegerField(default=0)
 
    class Meta:
        unique_together = ('product', 'name')
 
    def __str__(self):
        return f"{self.product.name} — {self.name}"