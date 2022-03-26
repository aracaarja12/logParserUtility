import pytest
import sys
from pathlib import PurePath

@pytest.fixture(scope="session")
def script_name(): 
    return PurePath(sys.argv[0]).parts[-1]