from pydantic import BaseModel


class UpdateDeliveryDto(BaseModel):
    delivery_id: int
    type: str | None
    status: str | None
    parcel_comp_name: str | None
    parcel_comp_id: str | None
    parcel_num: str | None
    exchange_reason: str | None
    return_reason: str | None


class TrackDeliveryDto(BaseModel):
    carrier_id: str
    tracking_number: str
