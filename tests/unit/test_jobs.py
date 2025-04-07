import responses
import pytest
from datetime import datetime, timezone

from synthex import Synthex
from synthex.consts import API_BASE_URL, LIST_JOBS_ENDPOINT
from synthex.models import ListJobsResponseModel
from synthex.exceptions import AuthenticationError


@responses.activate
def test_list_jobs_success(synthex: Synthex):
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{LIST_JOBS_ENDPOINT}",
        json={
            "status_code": 200,
            "status": "success",
            "message": "Jobs retrieved successfully",
            "data": {
                "total": 1,
                "jobs": [{
                    "id": "abc123",
                    "name": "Test name",
                    "description": "Test description",
                    "datapoint_num": 10,
                    "output_domain": "Test domain",
                    "status": "In Progress",
                    "created_at": datetime(2025, 3, 30, 16, 43, 37, 690586, tzinfo=timezone.utc).isoformat()
                }]
            }
        },
        status=200
    )

    jobs_info = synthex.jobs.list()

    assert isinstance(jobs_info, ListJobsResponseModel), "Jobs info is not of type ListJobsResponseModel."
    assert jobs_info.total == 1, "Total jobs count is not 1."
    assert jobs_info.jobs[0].name == "Test name", "Job name is not 'Test name'."
    assert jobs_info.jobs[0].description == "Test description", "Job description is not 'Test description'."
    assert jobs_info.jobs[0].datapoint_num == 10, "Job datapoint_num is not 10."
    

@responses.activate
def test_list_jobs_no_jobs_success(synthex: Synthex):
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{LIST_JOBS_ENDPOINT}",
        json={
            "status_code": 200,
            "status": "success",
            "message": "Jobs retrieved successfully",
            "data": {
                "total": 0,
                "jobs": []
            }
        },
        status=200
    )

    jobs_info = synthex.jobs.list()

    assert isinstance(jobs_info, ListJobsResponseModel), "Jobs info is not of type ListJobsResponseModel."
    assert jobs_info.total == 0, "Total jobs count is not 0."
    assert jobs_info.jobs == [], "Jobs list is not empty."
    
    
@responses.activate
def test_list_jobs_401_failure(synthex: Synthex):
    
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/{LIST_JOBS_ENDPOINT}",
        json={"error": "unauthorized"},
        status=401
    )

    try:
        with pytest.raises(AuthenticationError):
            synthex.jobs.list()
    except AssertionError:
        pytest.fail("Expected AuthenticationError when API returns 401")