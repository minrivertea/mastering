from django import template
from mastering.shop.models import Product, Category

register = template.Library()


def nav_selected(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'selected'
    return ''

register.simple_tag(nav_selected)

def product_nav(request, product, category):
    if category in product:
        return True
    return False

register.simple_tag(product_nav)