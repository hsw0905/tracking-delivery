from inject import clear_and_configure, Binder


def configure_app(binder: Binder):
    service_to_bind = [
    ]

    for service in service_to_bind:
        binder.bind_to_provider(service, service)


def init_provider():
    clear_and_configure(configure_app)