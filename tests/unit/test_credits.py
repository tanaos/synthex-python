import responses
import pytest

from synthex import Synthex
from synthex.consts import API_BASE_URL, GET_PROMOTIONAL_CREDITS_ENDPOINT
from synthex.models import CreditModel
from synthex.exceptions import NotFoundError, AuthenticationError


@responses.activate
def test_promotional_success(synthex: Synthex, ):    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{GET_PROMOTIONAL_CREDITS_ENDPOINT}",
        json={
            "status_code": 200,
            "status": "success",
            "message": "Credits retrieved successfully",
            "data": {
                "amount": 100,
                "currency": "USD",
            }
        },
        status=200
    )

    credits_info = synthex.credits.promotional()

    assert isinstance(credits_info, CreditModel)
    assert credits_info.amount== 100
    assert credits_info.currency == "USD"
    
    
@responses.activate
def test_promotional_401_failure(synthex: Synthex):
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{GET_PROMOTIONAL_CREDITS_ENDPOINT}",
        json={"error": "unauthorized"},
        status=401
    )

    with pytest.raises(AuthenticationError):
        synthex.credits.promotional()


@responses.activate
def test_promotional_404_failure(synthex: Synthex):
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{GET_PROMOTIONAL_CREDITS_ENDPOINT}",
        json={
            "status_code": 404,
            "status": "error",
            "message": "Not found",
            "details": None
        },
        status=404
    )

    with pytest.raises(NotFoundError):
        synthex.credits.promotional()