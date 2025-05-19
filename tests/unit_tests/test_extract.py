import pytest
from etl.extract.extract import main as extract_main

def test_extract_runs_without_errors():
    """Test that the extract main function runs without errors."""
    try:
        extract_main()
    except Exception as e:
        pytest.fail(f"extract_main() raised an exception: {e}")
