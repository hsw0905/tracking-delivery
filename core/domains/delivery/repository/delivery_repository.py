from sqlalchemy import select, update
from sqlalchemy.exc import DatabaseError

from app.exceptions.base import InternalServerErrorException
from app.extensions.database.sqlalchemy import session
from app.utils.log_helper import logger_
from core.domains.delivery.dto.delivery_dto import UpdateDeliveryDto
from core.domains.delivery.entity.delivery_entity import DeliveryEntity
from core.persistence.models.delivery_model import DeliveryModel

logger = logger_.getLogger(__name__)


class DeliveryRepository:
    def find_by_id(self, delivery_id: int | None) -> DeliveryEntity | None:
        if not delivery_id:
            return None

        statement = (
            select(DeliveryModel).where(DeliveryModel.id == delivery_id)
        )

        response = session.execute(statement).scalar()

        if response:
            return response.to_entity()
        return None

    def save(self, delivery: DeliveryModel) -> None:
        try:
            session.add(delivery)
        except DatabaseError as e:
            logger.error(f"[DeliveryRepository][save]: error, {e.detail}")
            session.rollback()
            raise InternalServerErrorException

    def patch(self, dto: UpdateDeliveryDto) -> None:
        update_dict = dict()
        dto_dict = dto.model_dump()
        for key, value in dto_dict.items():
            if key != "delivery_id" and value is not None:
                update_dict.update({key: value})

        try:
            statement = (
                update(DeliveryModel)
                .where(DeliveryModel.id == dto.delivery_id)
                .values(update_dict)
            )
            session.execute(statement)
        except DatabaseError as e:
            logger.error(f"[DeliveryRepository][patch]: error, {e.detail}")
            session.rollback()
            raise InternalServerErrorException
