from http import HTTPStatus

import inject

from app.extensions.database.transactional import Transactional
from app.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput
from core.domains.delivery.dto.delivery_dto import UpdateDeliveryDto
from core.domains.delivery.repository.delivery_repository import DeliveryRepository


class UpdateDeliveryUseCase:
    @inject.autoparams()
    def __init__(self, delivery_repo: DeliveryRepository):
        self._delivery_repo = delivery_repo

    @Transactional()
    def execute(self, dto: UpdateDeliveryDto) -> UseCaseSuccessOutput | UseCaseFailureOutput:
        delivery = self._delivery_repo.find_by_id(delivery_id=dto.delivery_id)

        if not delivery:
            return UseCaseFailureOutput(type_="0010", message="Not found", code=HTTPStatus.NOT_FOUND)

        self._delivery_repo.patch(dto=dto)

        return UseCaseSuccessOutput()
