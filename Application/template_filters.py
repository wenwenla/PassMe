from django.template.defaultfilters import register


@register.filter
def get_item(dic, key):
    return dic.get(key)
