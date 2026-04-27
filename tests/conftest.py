import copy
import pytest

from src.app import activities

# Store original activities for reset
original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state after each test."""
    yield
    # Reset after test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))