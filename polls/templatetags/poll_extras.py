from django import template


#------------------------------------------------------------------
# To fix price appearance in front-end

register = template.Library()


@register.filter(name='fix_currency')
def fix_currency(value):
    int_value = int(value)
    return '{:,}'.format(int_value) + ' تومان'
