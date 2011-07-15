from django.conf import settings
from mastering.shop.models import *



def common(request):
    from mastering import settings
    context = {}
    context['ga_is_on'] = settings.GA_IS_ON
    return context


def nav_objects(request):
    categories = Category.objects.all()
    nav_objects = []
    for category in categories:
        if category.parent is None:
            nav_objects.append(category)
    return {'nav_objects': nav_objects}