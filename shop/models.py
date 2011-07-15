from django.db import models
from django.shortcuts import get_object_or_404
import logging
from datetime import datetime

from slugify import smart_slugify
from mastering import settings

from tinymce import models as tinymce_models




class ShopSettings(models.Model):
    ga_tracking_code = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='images/', blank=True, null=True,
        help_text="Should be exactly 300 x 140px")
    homepage_title = models.CharField(max_length=200, blank=True, null=True)
    homepage_description = tinymce_models.HTMLField()
    homepage_meta_description = models.TextField(blank=True, null=True)
    product_page_description = tinymce_models.HTMLField(blank=True, null=True)
    show_prices = models.BooleanField(default=False)
    #main_homepage_image = models.ImageField(upload_to="images/", blank=True, null=True,
    #    help_text="Should be exactly 700px wide")
    site_email = models.CharField(max_length=200, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=80)
    description = tinymce_models.HTMLField()
    meta_description = models.CharField(max_length=200, blank=True, null=True)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    parent = models.ForeignKey("self", blank=True, null=True)
    hot_item = models.ForeignKey('Product', related_name='hot-item', blank=True, null=True)
    
    def __unicode__(self):
        return self.name
      
    def get_absolute_url(self):
        return "/products/%s/" % self.slug  #important, do not change
    
    def get_children(self):
        children = Category.objects.filter(parent=self)
        return children

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=80)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.CharField(max_length=200, blank=True, null=True)		
    short_description = tinymce_models.HTMLField()
    description = tinymce_models.HTMLField()
    body_text = tinymce_models.HTMLField()
    image = models.ImageField(upload_to='images/product-photos')
    image_2 = models.ImageField(upload_to='images/product-photos', blank=True, null=True)
    image_2_caption = models.CharField(max_length=200, blank=True)
    image_3 = models.ImageField(upload_to='images/product-photos', blank=True, null=True)
    image_3_caption = models.CharField(max_length=200, blank=True)
    image_4 = models.ImageField(upload_to='images/product-photos', blank=True, null=True)
    image_4_caption = models.CharField(max_length=200, blank=True)
    image_5 = models.ImageField(upload_to='images/product-photos', blank=True, null=True)
    image_5_caption = models.CharField(max_length=200, blank=True)
    category = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
     
    def get_category(self):
        categories = self.category.all()
        category = []
        for c in self.category.all():
            if c.parent:
                category.append(dict(
                    category=str(c.slug),
                    parent=str(c.parent.slug),
                ))
            else:
                category.append(dict(
                    category="",
                    parent=str(c.slug),
                ))
        return category[0]

        
    def get_absolute_url(self):
        return "/%s/" % self.slug  #important, do not change

            
class Testimonial(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=200)
    full_text = models.TextField()
    short_text = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.short_text       
   
class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=80)
    description = models.CharField(max_length=200)
    full_text = tinymce_models.HTMLField()
    date_published = models.DateTimeField(default=datetime.now())
    is_draft = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/news', blank=True)
    
    def __unicode__(self):
        return self.title     
            
         


