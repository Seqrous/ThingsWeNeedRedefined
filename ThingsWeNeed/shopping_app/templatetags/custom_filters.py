from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def reverse(value):
    value.reverse()
    return value

def products(value, arg):
    arg = mark_safe(arg)
    arg = arg.strip()

    if arg=="pending":
        """ 
        Return a collection of products that are
        not wishes (is_wish==False) and haven't been 
        bought yet (bought_by==None) 
        """
        products = []
        for product in list(value):
            if product.bought_by is None and not product.is_wish:
                products.append(product)

        return products
    elif arg=="bought":
        """ 
        Return a collection of products that are
        not wishes (is_wish==False) and have been 
        bought already (bought_by!=None) 
        """
        products = []
        for product in list(value):
            if not product.bought_by is None and not product.is_wish:
                products.append(product)
                
        return products
    elif arg=="wishes":
        """ 
        Return a collection of products that are
        wishes (is_wish==True) and haven't been 
        bought yet (bought_by==None) 
        """
        products = []
        for product in list(value):
            if product.bought_by is None and product.is_wish:
                products.append(product)

        return products
    else:
        return None

register.filter('reverse', reverse)
register.filter('products', products)