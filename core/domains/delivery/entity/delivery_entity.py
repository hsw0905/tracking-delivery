from datetime import datetime

from pydantic import BaseModel


class DeliveryEntity(BaseModel):
    id: int
    type: str
    status: str
    parcel_company_name: str
    parcel_company_id: str
    parcel_num: str
    created_at: datetime
    updated_at: datetime
