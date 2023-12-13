from pydantic import BaseModel, StrictStr


class UpdateDeliveryResponseSchema(BaseModel):
    result: StrictStr
