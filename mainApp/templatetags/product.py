from django import template
from mainApp.models import Checkout,CheckOutProduct
register = template.Library()

@register.filter("checkcolor")
def checkcolor(color,item):
    flag = False
    for i in color.split(","):
        if(i==item):
            flag = True
            break
    return flag

@register.filter("checksize")
def checksize(size,item):
    flag = False
    for i in size.split(","):
        if(i==item):
            flag = True
            break
    return flag


@register.filter("orderItems")
def orderItems(request, num):
    check = Checkout.objects.get(id=num)
    p = CheckOutProduct.objects.filter(checkout=check)
    return p


@register.filter("Stock")
def Stock(request, data):
    if(data=="In Stock"):
        return True
    else:
        return False