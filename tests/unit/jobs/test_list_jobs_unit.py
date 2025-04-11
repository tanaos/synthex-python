import responses
import pytest
from datetime import datetime, timezone

from synthex import Synthex
from synthex.endpoints import API_BASE_URL, LIST_JOBS_ENDPOINT
from synthex.models import ListJobsResponseModel
from synthex.exceptions import AuthenticationError


@pytest.mark.unit
@responses.activate
def test_list_jobs_success(synthex: Synthex):
    """
    Test the successful retrieval of a list of jobs using the `list` method of the `Synthex` class.
    This test mocks an HTTP GET request to the jobs endpoint and verifies that the response is correctly
    parsed into a `ListJobsResponseModel` object. It checks the following:
    - The response is of the expected type (`ListJobsResponseModel`).
    - The total number of jobs matches the expected value.
    - The attributes of the first job in the list (name, description, datapoint_num) match the expected values.
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
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
    

@pytest.mark.unit
@responses.activate
def test_list_jobs_no_jobs_success(synthex: Synthex):
    """
    Test the successful retrieval of an empty list of jobs using the `list` method of the `Synthex` class.
    This test mocks an HTTP GET request to the jobs endpoint and verifies that the response is correctly
    parsed into a `ListJobsResponseModel` object. It checks the following:
    - The response is of the expected type (`ListJobsResponseModel`).
    - The total number of jobs is 0.
    - The jobs list is empty.
    Args:
        synthex (Synthex): An instance of the Synthex class used to invoke the `generate_data` method.
        generate_data_params (dict[Any, Any]): A dictionary containing the required parameters 
    """
    
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
    

@pytest.mark.unit
@responses.activate
def test_list_jobs_401_failure(synthex: Synthex):
    """
    Test case for handling a 401 Unauthorized response when listing jobs.
    This test verifies that the `list` method of the `jobs` module in the `Synthex`
    client raises an `AuthenticationError` when the API responds with a 401 status code.
    Steps:
    1. Mock the API response to return a 401 status code with an "unauthorized" error message.
    2. Attempt to call the `list` method on the `jobs` module.
    3. Assert that an `AuthenticationError` is raised.
    4. If the error is not raised, the test fails with an appropriate message.
    Args:
        synthex (Synthex): An instance of the Synthex client.
    """
    
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
    