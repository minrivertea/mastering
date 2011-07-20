from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from django.http import HttpResponseRedirect 
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import urllib
import urllib2
import xml.etree.ElementTree as etree

from PIL import Image
from cStringIO import StringIO
import os, md5
import datetime
import uuid

from mastering.shop.models import *
from mastering.shop.forms import *
from mastering.slugify import smart_slugify


#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )

import json, socket

def GetCountry(request):
    # this is coming from http://ipinfodb.com JSON api
    # the variables
    apikey = settings.IPINFO_APIKEY 
    ip = request.META.get('REMOTE_ADDR')
    baseurl = "http://api.ipinfodb.com/v3/ip-country/?key=%s&ip=%s&format=json" % (apikey, ip)
    urlobj = urllib2.urlopen(baseurl)
    
    # get the data
    url = baseurl + "?" + apikey + "?"
    data = urlobj.read()
    urlobj.close()
    datadict = json.loads(data)
    return datadict


# the homepage view
def index(request):
    # load variables       
    products = Product.objects.filter(is_active=True, featured=True)
    reviews = Testimonial.objects.all().order_by('?')[:1]
    country = GetCountry(request)
    print GetCountry(request)['ipAddress']
    return render(request, "shop/home.html", locals())
    

# view for a top level category
def category(request, cat):
    category = get_object_or_404(Category, slug=cat)
    reviews = Testimonial.objects.all().order_by('?')[:1]
    children = category.get_children()
    products = Product.objects.all().order_by('name')
    products_list = []
    for p in products:
        if category in p.category.all():
            products_list.append(p)
        for c in children:
            if c in p.category.all():
                products_list.append(p)
    
    return render(request, "shop/category.html", locals())

# view for a sub-level category
def sub_category(request, cat, sub_cat):
    category = get_object_or_404(Category, slug=sub_cat)
    products_list = Product.objects.filter(category=category)
    return render(request, "shop/category.html", locals())
  
  
def product(request, cat=None, sub_cat=None, slug=None):
    product = get_object_or_404(Product, slug=slug)

    return render(request, "shop/product.html", locals())
   
   
def all_news(request):
    news = News.objects.filter(is_draft=False).order_by('-date_published')
    return render(request, "shop/news.html", locals())

def news_item(request, slug):
    item = get_object_or_404(News, slug=slug)
    return render(request, "shop/news_item.html", locals())

    
def contact_us(request):
    try:
        if request.session['MESSAGE'] == "1":
            message = True
            request.session['MESSAGE'] = ""
    except:
        pass 
        
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            # get cleaned data from form submission
            message = form.cleaned_data['your_message']
            your_name = form.cleaned_data['your_name']
            your_email = form.cleaned_data['your_email']
            phone = form.cleaned_data['phone_number']
            country = form.cleaned_data['country']
            
            # create email
            body = render_to_string('shop/emails/contact_template.txt', {
            	 'message': message,
            	 'your_email': your_email,
            	 'your_name': your_name,
            	 'phone': phone,
            	 'country': country,
            })

            recipient = settings.SITE_EMAIL
            sender = settings.SITE_EMAIL
            subject_line = "Mastering-outdoors.com - Website Contact Submission"
                
            send_mail(
                          subject_line, 
                          body, 
                          sender,
                          [recipient], 
                          fail_silently=False
            )
            
            
            url = reverse('contact_us')
            request.session['MESSAGE'] = "1"
            return HttpResponseRedirect(url) 
    else:
        form = ContactForm() 
    
    return render(request, "shop/forms/contact_form.html", locals())        

@login_required
def create_products(request):
    if request.method == 'POST':
        form = CreateProductsForm(request.POST, request.FILES)
        if form.is_valid():
            
            number = form.cleaned_data['number']
            
            # sort out the photo first
            photo = request.FILES['image']
            image_content = photo.read()
            image = Image.open(StringIO(image_content))
            format = image.format
            format = format.lower().replace('jpeg', 'jpg')
            filename = md5.new(image_content).hexdigest() + '.' + format
            # Save the image
            path = os.path.join(settings.MEDIA_ROOT, 'images/product-photos', filename)
            # check that the dir of the path exists
            dirname = os.path.dirname(path)
            if not os.path.isdir(dirname):
                try:
                    os.mkdir(dirname)
                except IOError:
                    raise IOError, "Unable to create the directory %s" % dirname
            open(path, 'w').write(image_content)
              
            
            loop_count = 0
            while loop_count < int(number):
                slug = "%s-%s" % (form.cleaned_data['slug'], loop_count)
                name = "%s-%s" % (form.cleaned_data['name'], loop_count)
                category = get_object_or_404(Category, name=form.cleaned_data['category'])
                creation_args = {
                    'name': name,
                    'slug': slug,
                    'meta_title': form.cleaned_data['meta_title'],
                    'meta_description': form.cleaned_data['meta_description'],
                    'short_description': form.cleaned_data['short_description'],
                    'description': form.cleaned_data['description'],
                    'body_text': form.cleaned_data['body_text'],
                    'image': 'images/product-photos/%s' % filename,
                    'is_active': False,
                }
                
                product = Product.objects.create(**creation_args)
                product.category.add(category)
                product.save()
                loop_count += 1
                print loop_count
            
            return HttpResponseRedirect("/")
            
            
    
    else:
        form = CreateProductsForm()
    
    
    return render(request, "shop/forms/create_products_form.html", locals())
    