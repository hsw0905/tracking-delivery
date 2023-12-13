from sqlalchemy.orm import scoped_session, Session

from core.domains.delivery.dto.delivery_dto import UpdateDeliveryDto
from core.domains.delivery.enum.delivery_enum import DeliveryStatus
from core.domains.delivery.repository.delivery_repository import DeliveryRepository
from core.domains.delivery.use_case.v1.delivery_use_case import UpdateDeliveryUseCase
from tests.seeder.factory import DeliveryModelFactory


def test_should_patch_status(session: scoped_session[Session]):
    delivery = DeliveryModelFactory.create()
    session.commit()

    dto = UpdateDeliveryDto(
        delivery_id=delivery.id,
        status=DeliveryStatus.DELIVERING.value[0],
        type=None,
        parcel_comp_name=None,
        parcel_comp_id=None,
        parcel_num=None,
        exchange_reason=None,
        return_reason=None
    )
    repository = DeliveryRepository()
    use_case = UpdateDeliveryUseCase()

    use_case.execute(dto=dto)

    result = repository.find_by_id(delivery_id=delivery.id)

    assert result.status == DeliveryStatus.DELIVERING.value[0]
