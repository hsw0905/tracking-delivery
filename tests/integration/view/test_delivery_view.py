from http import HTTPStatus

from flask import url_for
from sqlalchemy.orm import scoped_session, Session

from core.domains.delivery.enum.delivery_enum import DeliveryStatus
from core.domains.delivery.repository.delivery_repository import DeliveryRepository
from tests.seeder.factory import DeliveryModelFactory


def test_should_patch_status(session: scoped_session[Session], app, client) -> None:
    delivery = DeliveryModelFactory.create()
    session.commit()

    with app.test_request_context():
        response = client.patch(
            url_for(
                "tracking-delivery.update_delivery_view",
                delivery_id=delivery.id,
            ),
            json={
                "status": DeliveryStatus.DELIVERING.value[0]
            }
        )

    repository = DeliveryRepository()
    result = repository.find_by_id(delivery_id=delivery.id)

    assert response.json["data"]["result"] == "success"
    assert result.status == DeliveryStatus.DELIVERING.value[0]
