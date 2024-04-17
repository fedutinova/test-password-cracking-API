from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status
import logging


logger = logging.getLogger(__name__)


class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ident = request.user.id
        key = f"ratelimit_{ident}"
        current_count = cache.get(key, 0)

        limit = getattr(settings, 'RATE_LIMIT', 10)
        interval = getattr(settings, 'LIMIT_INTERVAL', 60)

        if current_count >= limit:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if current_count == 0:
            cache.set(key, 1, timeout=interval)
        else:
            cache.incr(key)

        return None
