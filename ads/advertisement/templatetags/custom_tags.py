from django import template
from advertisement.models import Response


register = template.Library()


@register.simple_tag()
def get_quantity_response(ads_id):
    return len(Response.objects.filter(ads=ads_id))
