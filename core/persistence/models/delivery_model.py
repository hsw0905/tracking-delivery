from sqlalchemy import BigInteger, Integer, VARCHAR, DateTime, func
from sqlalchemy.orm import mapped_column

from app.extensions.database.sqlalchemy import db
from core.domains.delivery.entity.delivery_entity import DeliveryEntity


class DeliveryModel(db.Model):
    __tablename__ = "deliveries"

    id = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    type = mapped_column(VARCHAR(1))
    status = mapped_column(VARCHAR(1))
    parcel_company_name = mapped_column(VARCHAR(50))
    parcel_company_id = mapped_column(VARCHAR(50))
    parcel_num = mapped_column(VARCHAR(50))
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def to_entity(self) -> DeliveryEntity:
        return DeliveryEntity(
            id=self.id,
            type=self.type,
            status=self.status,
            parcel_company_name=self.parcel_company_name,
            parcel_company_id=self.parcel_company_id,
            parcel_num=self.parcel_num,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
