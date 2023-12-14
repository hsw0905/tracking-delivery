from http import HTTPStatus

import inject
import requests
from flask import current_app

from app.extensions.database.transactional import Transactional
from app.use_case_output import UseCaseSuccessOutput, UseCaseFailureOutput
from core.domains.delivery.dto.delivery_dto import UpdateDeliveryDto, TrackDeliveryDto
from core.domains.delivery.entity.delivery_entity import DeliveryEntity
from core.domains.delivery.enum.delivery_enum import DeliveryStatus
from core.domains.delivery.repository.delivery_repository import DeliveryRepository


class UpdateDeliveryUseCase:
    @inject.autoparams()
    def __init__(self, delivery_repo: DeliveryRepository):
        self._delivery_repo = delivery_repo

    @Transactional()
    def execute(
        self, dto: UpdateDeliveryDto
    ) -> UseCaseSuccessOutput | UseCaseFailureOutput:
        delivery = self._delivery_repo.find_by_id(delivery_id=dto.delivery_id)

        if not delivery:
            return UseCaseFailureOutput(
                type_="0010", message="Not found", code=HTTPStatus.NOT_FOUND
            )

        self._delivery_repo.patch(dto=dto)

        return UseCaseSuccessOutput()


class TrackDeliveryUseCase:
    @inject.autoparams()
    def __init__(
        self, delivery_repo: DeliveryRepository, update_use_case: UpdateDeliveryUseCase
    ):
        self._delivery_repo = delivery_repo
        self._update_use_case = update_use_case

    def execute(
        self, dto: TrackDeliveryDto
    ) -> UseCaseSuccessOutput | UseCaseFailureOutput:
        delivery = self._delivery_repo.find_by_parcel_company_id_and_number(
            parcel_company_id=dto.carrier_id, parcel_num=dto.tracking_number
        )

        if not delivery:
            return UseCaseFailureOutput(
                type_="0010", message="Not found", code=HTTPStatus.NOT_FOUND
            )

        token_response = self._request_token()
        if token_response.raise_for_status():
            return UseCaseFailureOutput(
                type_="0100", message="Failed get token", code=HTTPStatus.NOT_FOUND
            )

        access_token = token_response.json().get("access_token")

        track_response = self._request_track(token=access_token, delivery=delivery)

        if track_response.raise_for_status():
            return UseCaseFailureOutput(
                type_="0100", message="Failed tracking", code=HTTPStatus.NOT_FOUND
            )

        status = track_response.json()["data"]["track"]["lastEvent"]["status"].get(
            "code"
        )

        update_dto = UpdateDeliveryDto(
            delivery_id=delivery.id,
            type=None,
            status=DeliveryStatus.DELIVERY_DONE.value[0]
            if status == "DELIVERED"
            else DeliveryStatus.DELIVERING.value[0],
            parcel_comp_name=None,
            parcel_comp_id=None,
            parcel_num=None,
            exchange_reason=None,
            return_reason=None,
        )
        return self._update_use_case.execute(dto=update_dto)

    def _request_track(self, token: str, delivery: DeliveryEntity):
        url = current_app.config.get("DELIVERY_TRACKER_URI") + "/graphql"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        query = """
        query Track($carrierId: ID!, $trackingNumber: String!) {
        track(carrierId: $carrierId, trackingNumber: $trackingNumber) {
            lastEvent {
                time
                status {
                    code
                    name
                    }
                description
                }
            }
        }
        """
        variables = {
            "carrierId": delivery.parcel_company_id,
            "trackingNumber": delivery.parcel_num,
        }

        return requests.post(
            url, headers=headers, json={"query": query, "variables": variables}
        )

    def _request_token(self):
        url = current_app.config.get("DELIVERY_TRACKER_AUTH_URI") + "/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Apollo-Require-Preflight": "true",
        }
        payload = {
            "grant_type": "client_credentials",
            "client_id": current_app.config.get("TRACK_CLIENT_ID"),
            "client_secret": current_app.config.get("TRACK_CLIENT_SECRET"),
        }

        return requests.post(url, headers=headers, data=payload)
