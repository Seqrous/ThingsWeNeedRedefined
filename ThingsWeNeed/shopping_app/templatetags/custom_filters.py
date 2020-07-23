from django import template

register = template.Library()

def reverse(value):
    value.reverse()
    return value

register.filter('reverse', reverse)