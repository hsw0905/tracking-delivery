from http import HTTPStatus

from flask import request
from werkzeug import Response

from app.api.views import api
from app.api.requests.v1.delivery_request import (
    UpdateDeliveryRequestSchema,
    TrackDeliveryRequestSchema,
)
from app.api.responses import failure_response
from app.api.responses.presenters.v1.delivery_presenter import (
    UpdateDeliveryPresenter,
    TrackDeliveryPresenter,
)
from app.exceptions.base import InvalidRequestException
from app.use_case_output import UseCaseFailureOutput, FailureType
from core.domains.delivery.use_case.v1.delivery_use_case import (
    UpdateDeliveryUseCase,
    TrackDeliveryUseCase,
)


@api.patch("/v1/deliveries/<int:delivery_id>")
def update_delivery_view(delivery_id: int) -> Response:
    try:
        dto = UpdateDeliveryRequestSchema(
            delivery_id=delivery_id, **request.get_json()
        ).validate_request_and_make_dto()
    except InvalidRequestException as e:
        return failure_response(
            UseCaseFailureOutput(
                type_=FailureType.INVALID_REQUEST_ERROR,
                code=HTTPStatus.BAD_REQUEST,
                message=f"Invalid request parameter: {e.message}",
            )
        )
    return UpdateDeliveryPresenter().transform(UpdateDeliveryUseCase().execute(dto=dto))


@api.post("/v1/deliveries/tracking")
def track_callback_view():
    try:
        body = request.json
        dto = TrackDeliveryRequestSchema(
            carrier_id=body["carrierId"], tracking_number=body["trackingNumber"]
        ).validate_request_and_make_dto()
    except InvalidRequestException as e:
        return failure_response(
            UseCaseFailureOutput(
                type_=FailureType.INVALID_REQUEST_ERROR,
                code=HTTPStatus.BAD_REQUEST,
                message=f"Invalid request parameter: {e.message}",
            )
        )
    return TrackDeliveryPresenter().transform(TrackDeliveryUseCase().execute(dto=dto))
