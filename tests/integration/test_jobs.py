import pytest

from synthex import Synthex
from synthex.models import ListJobsResponseModel


@pytest.mark.integration
def test_list_jobs(synthex: Synthex):
    """
    Test the `list` method of the `jobs` attribute in the `Synthex` class.
    This test verifies that the `list` method of `synthex.jobs` returns an 
    instance of `ListJobsResponseModel`.
    Args:
        synthex (Synthex): An instance of the `Synthex` class.
    Asserts:
        The returned value from `synthex.jobs.list()` is an instance of 
        `ListJobsResponseModel`.
    """
    
    jobs_info = synthex.jobs.list()
    print("jobs_info: ", jobs_info)
        
    assert isinstance(jobs_info, ListJobsResponseModel)