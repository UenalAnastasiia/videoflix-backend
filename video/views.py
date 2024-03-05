from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .tasks import create_backup_export


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# @cache_page(CACHE_TTL)

def export_backend_view(request):
    backup_json = create_backup_export()
    return HttpResponse(backup_json)