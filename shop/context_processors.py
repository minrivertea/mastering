from django.conf import settings
from mastering.shop.models import *
from mastering.shop.views import GetCountry


def common(request):
    from mastering import settings
    context = {}
    try:
        context['shopsettings'] = get_object_or_404(ShopSettings, pk=1)
    except:
        pass
    context['ga_is_on'] = settings.GA_IS_ON
#    countrycode = GetCountry(request)['countryCode']
#    if countrycode == "US":
#       context['howdy'] = True
#    if countrycode == "IN":
#       context['india'] = True
    return context


def nav_objects(request):
    categories = Category.objects.all()
    nav_objects = []
    for category in categories:
        if category.parent is None:
            nav_objects.append(category)
    return {'nav_objects': nav_objects}