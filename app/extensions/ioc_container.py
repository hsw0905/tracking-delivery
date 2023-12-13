from inject import clear_and_configure, Binder

from core.domains.delivery.repository.delivery_repository import DeliveryRepository


def configure_app(binder: Binder):
    service_to_bind = [
        DeliveryRepository,
    ]

    for service in service_to_bind:
        binder.bind_to_provider(service, service)


def init_provider():
    clear_and_configure(configure_app)