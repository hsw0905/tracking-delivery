from sqlalchemy import BigInteger, Integer, VARCHAR, Index, DateTime, func
from sqlalchemy.orm import mapped_column

from app import db


class DeliveryModel(db.Model):
    __tablename__ = "deliveries"
    __table_args__ = (
        Index("delivery_type_status_idx", "dlv_type", "dlv_status")
    )

    id = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    type = mapped_column(VARCHAR(1), index=True)
    status = mapped_column(VARCHAR(1))
    parcel_company_name = mapped_column(VARCHAR(50))
    parcel_company_id = mapped_column(VARCHAR(50))
    parcel_num = mapped_column(VARCHAR(40))
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)