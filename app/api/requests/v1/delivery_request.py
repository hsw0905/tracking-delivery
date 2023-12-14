from pydantic import BaseModel, field_validator, ValidationError

from app.exceptions.base import InvalidRequestException
from app.utils.log_helper import logger_
from core.domains.delivery.dto.delivery_dto import UpdateDeliveryDto, TrackDeliveryDto

logger = logger_.getLogger(__name__)


class UpdateDeliverySchema(BaseModel):
    delivery_id: int
    type: str | None
    status: str | None
    parcel_comp_name: str | None
    parcel_comp_id: str | None
    parcel_num: str | None
    exchange_reason: str | None
    return_reason: str | None

    @field_validator("exchange_reason")
    def validate_exchange_reason(cls, exchange_reason):
        exchange_reasons = ["색상 변경", "상품 파손", "상품 불량", "오배송", "상품 구성품 누락", "상품설명과 상이", "기타"]

        if exchange_reason is None:
            return None

        if exchange_reason in exchange_reasons:
            return exchange_reason
        raise ValueError("must contain reason in exchange reason_list or None")

    @field_validator("return_reason")
    def validate_return_reason(cls, return_reason):
        return_reasons = ["주문 실수", "단순 변심", "서비스 불만족", "배송 지연", "상품 품절", "배송 누락", "상품설명과 상이", "기타"]

        if return_reason is None:
            return None

        if return_reason in return_reasons:
            return return_reason
        raise ValueError("must contain reason in return reason_list or None")


class UpdateDeliveryRequestSchema:
    def __init__(self, delivery_id,
                 type=None,
                 status=None,
                 parcel_comp_name=None,
                 parcel_comp_id=None,
                 parcel_num=None,
                 exchange_reason=None,
                 return_reason=None):
        self.delivery_id = delivery_id
        self.type = type
        self.status = status
        self.parcel_comp_name = parcel_comp_name if parcel_comp_name else None
        self.parcel_comp_id = parcel_comp_id if parcel_comp_id else None
        self.parcel_num = parcel_num if parcel_num else None
        self.exchange_reason = exchange_reason
        self.return_reason = return_reason

    def validate_request_and_make_dto(self):
        try:
            schema = UpdateDeliverySchema(
                delivery_id=self.delivery_id,
                type=self.type,
                status=self.status,
                parcel_comp_name=self.parcel_comp_name,
                parcel_comp_id=self.parcel_comp_id,
                parcel_num=self.parcel_num,
                exchange_reason=self.exchange_reason,
                return_reason=self.return_reason
            ).model_dump()
            return UpdateDeliveryDto(**schema)
        except ValidationError as e:
            logger.error(
                f"[UpdateDeliveryRequestSchema][validate_request_and_make_dto] error : {e}"
            )
            raise InvalidRequestException(message=e.errors())


class TrackDeliverySchema(BaseModel):
    carrier_id: str
    tracking_number: str


class TrackDeliveryRequestSchema:
    def __init__(self, carrier_id: str, tracking_number: str) -> None:
        self.carrier_id = carrier_id,
        self.tracking_number = tracking_number

    def validate_request_and_make_dto(self):
        try:
            schema = TrackDeliverySchema(
                carrier_id=self.carrier_id,
                tracking_number=self.tracking_number
            ).model_dump()
            return TrackDeliveryDto(**schema)
        except ValidationError as e:
            logger.error(
                f"[TrackDeliveryRequestSchema][validate_request_and_make_dto] error : {e}"
            )
            raise InvalidRequestException(message=e.errors())
