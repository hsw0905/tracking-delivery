from enum import Enum


class DisplayStatusEnum(Enum):
    def __new__(cls, code, name):
        obj = object.__new__(cls)
        obj.code = code
        obj.display_name = name
        return obj

    @classmethod
    def display_name(cls, code):
        for item in cls:
            if item.code == code:
                return item.display_name


class DeliveryType(Enum):
    DELIVERY = "1"  # 배송
    EXCHANGE = "2"  # 교환
    RETURN = "3"  # 반품


class DeliveryStatus(DisplayStatusEnum):
    DELIVERY_REQUEST_DONE = ("1", "배송신청완료")
    DELIVERING = ("2", "배송중")
    DELIVERY_DONE = ("3", "배송완료")


class ExchangeStatus(DisplayStatusEnum):
    EXCHANGE_REQUEST = ("1", "교환접수")
    EXCHANGE_DELIVERING = ("2", "교환배송중")
    EXCHANGE_DONE = ("3", "교환배송완료")


class ReturnStatus(DisplayStatusEnum):
    RETURN_REQUEST = ("1", "반품접수")
    WITHDRAWING = ("2", "회수중")
    WITHDRAW_DONE = ("3", "회수완료")
    RETURN_DONE = ("4", "반품완료")
