from http import HTTPStatus

from pydantic import ValidationError

from app.api.responses import failure_response, success_response
from app.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput, FailureType
from core.domains.delivery.schema.delivery_schema import (
    UpdateDeliveryResponseSchema,
    TrackDeliveryResponseSchema,
)


class UpdateDeliveryPresenter:
    def transform(self, output: UseCaseSuccessOutput | UseCaseFailureOutput):
        if isinstance(output, UseCaseSuccessOutput):
            try:
                schema = UpdateDeliveryResponseSchema(result=output.type)
            except ValidationError as e:
                return failure_response(
                    UseCaseFailureOutput(
                        code=FailureType.INTERNAL_SERVER_ERROR,
                        type_=FailureType.SYSTEM_ERROR,
                        message="response schema validation error",
                    ),
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            result = {
                "data": schema.model_dump(),
                "meta": output.meta,
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)


class TrackDeliveryPresenter:
    def transform(self, output: UseCaseSuccessOutput | UseCaseFailureOutput):
        if isinstance(output, UseCaseSuccessOutput):
            try:
                schema = TrackDeliveryResponseSchema(result=output.type)
            except ValidationError as e:
                return failure_response(
                    UseCaseFailureOutput(
                        code=FailureType.INTERNAL_SERVER_ERROR,
                        type_=FailureType.SYSTEM_ERROR,
                        message="response schema validation error",
                    ),
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            result = {
                "data": schema.model_dump(),
                "meta": output.meta,
            }
            return success_response(result=result)
        elif isinstance(output, UseCaseFailureOutput):
            return failure_response(output=output)
