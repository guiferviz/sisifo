import pytest


# we want to have pytest assert introspection in the sisifo package
pytest.register_assert_rewrite("sisifo")
