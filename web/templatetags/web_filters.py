from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django import template

register = template.Library()

@require_http_methods(['GET'])
@login_required
@register.filter(name="is_site_manager")
def is_site_manager(request):
    return request.groups.filter(name='Site Managers').exists()