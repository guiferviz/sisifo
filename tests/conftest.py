import pytest

import sisifo


@pytest.fixture
def data_collection():
    return sisifo.DataCollection()
