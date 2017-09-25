from .exceptions import ServiceNotFound

services = dict()


def get_default_service(key):
    if key == 'config':
        from . import configs as config_service
        return config_service
    raise ServiceNotFound(key)


def create_service(key, service=None):
    if service is None:
        service = get_default_service(key)
    services[key] = service

# TODO: add support for start/restart/stop service


def get_or_create_service(key):
    if key not in services:
        create_service(key)
    return services[key]
    
