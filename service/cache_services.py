from django.core.cache import cache

from service.models import ClientOfService
from config.settings import CASHED_ENABLED


def get_product_from_cache():
    if not CASHED_ENABLED:
        return ClientOfService.objects.all()
    key = "clients_list"
    clients = cache.get(key)
    if clients is not None:
        return clients
    products = ClientOfService.objects.all()
    cache.set(key, products)
    return clients
