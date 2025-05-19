import pytest
from etl.transform.transform import main as transform_main

def test_transform_runs_without_errors():
    """Test that the transform main function runs without errors."""
    try:
        transform_main()
    except Exception as e:
        pytest.fail(f"transform_main() raised an exception: {e}")
