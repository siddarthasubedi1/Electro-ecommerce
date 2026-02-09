from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

class Tag(models.Model):
    name= models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    
    name = models.CharField(max_length=50)
    old_price = models.DecimalField(max_digits=15,decimal_places=2,default=0.0)
    price = models.DecimalField(max_digits=15,decimal_places=2,default=0.0)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    all_products = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    new_arrivals = models.BooleanField(default=False)
    top_selling = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, related_name='products')
    tag = models.ManyToManyField(Tag, related_name='product_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name