from django import template

register = template.Library()

@register.filter
def has_profile_pic(user):
    return bool(user.profile_pic)