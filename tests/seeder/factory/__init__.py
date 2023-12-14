import factory

from core.domains.delivery.enum.delivery_enum import DeliveryType, DeliveryStatus
from core.persistence.models.delivery_model import DeliveryModel


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True


class DeliveryModelFactory(BaseFactory):
    class Meta:
        model = DeliveryModel

    id = factory.Sequence(lambda n: n + 1)
    type = DeliveryType.DELIVERY.value
    status = DeliveryStatus.DELIVERY_REQUEST_DONE.value[0]
    parcel_company_name = "CJ대한통운"
    parcel_company_id = "kr.cjlogistics"
    parcel_num = "1234567890"
