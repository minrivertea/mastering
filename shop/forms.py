from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from captcha.fields import CaptchaField


from mastering.shop.models import *

# handles the contact us form
class ContactForm(forms.Form):
    your_name = forms.CharField(required=True)
    your_email = forms.EmailField(required=True, error_messages={'required': 'Please enter a valid email address'})
    your_message = forms.CharField(widget=forms.Textarea, required=False)
    country = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    captcha = CaptchaField()


class CreateProductsForm(forms.Form):
    name = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    meta_title = forms.CharField(required=True)
    meta_description = forms.CharField(widget=forms.Textarea, required=True)
    short_description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    body_text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    image = forms.ImageField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    number = forms.CharField(required=True, help_text="The number of product items to create, eg. '25'")