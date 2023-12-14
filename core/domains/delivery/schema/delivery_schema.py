from pydantic import BaseModel, StrictStr


class UpdateDeliveryResponseSchema(BaseModel):
    result: StrictStr


class TrackDeliveryResponseSchema(BaseModel):
    result: StrictStr
