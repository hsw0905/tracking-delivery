from sqlalchemy.orm import scoped_session, Session

from core.domains.delivery.dto.delivery_dto import UpdateDeliveryDto
from core.domains.delivery.enum.delivery_enum import DeliveryStatus
from core.domains.delivery.repository.delivery_repository import DeliveryRepository
from tests.seeder.factory import DeliveryModelFactory


def test_should_find_by_id(session: scoped_session[Session]) -> None:
    delivery = DeliveryModelFactory.create()
    session.commit()

    repository = DeliveryRepository()
    result = repository.find_by_id(delivery_id=delivery.id)

    assert result.id == delivery.id
    assert result.type == delivery.type
    assert result.status == delivery.status
    assert result.parcel_company_name == delivery.parcel_company_name
    assert result.parcel_company_id == delivery.parcel_company_id
    assert result.parcel_num == delivery.parcel_num


def test_should_patch_status(session: scoped_session[Session]) -> None:
    delivery = DeliveryModelFactory.create()
    session.commit()

    repository = DeliveryRepository()
    repository.patch(dto=UpdateDeliveryDto(
        delivery_id=delivery.id,
        status=DeliveryStatus.DELIVERING.value[0],
        type=None,
        parcel_comp_name=None,
        parcel_comp_id=None,
        parcel_num=None,
        exchange_reason=None,
        return_reason=None
    ))
    result = repository.find_by_id(delivery_id=delivery.id)

    assert result.status == DeliveryStatus.DELIVERING.value[0]


def test_should_get_tracking_info(session: scoped_session[Session]) -> None:
    delivery = DeliveryModelFactory.create()
    session.commit()

    repository = DeliveryRepository()
    result = repository.find_by_parcel_company_id_and_number(parcel_company_id=delivery.parcel_company_id,
                                                             parcel_num=delivery.parcel_num)

    assert result.id == delivery.id
    assert result.parcel_company_id == delivery.parcel_company_id
    assert result.parcel_num == delivery.parcel_num
