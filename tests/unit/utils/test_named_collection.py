import sisifo.named_collection as named_collection

import pytest


@pytest.fixture
def surnames():
    return named_collection.BaseNamedCollection()


def test_base_named_collection_insert(surnames):
    surnames["Ignatius"] = "Reilly"
    assert surnames["Ignatius"] == "Reilly"


def test_base_named_collection_len(surnames):
    assert len(surnames) == 0
    surnames["Ignatius"] = "Reilly"
    surnames["Myrna"] = "Minkoff"
    assert len(surnames) == 2


def test_base_named_collection_items_loop(surnames):
    surnames["Ignatius"] = "Reilly"
    for k, v in surnames.items():
        assert k == "Ignatius"
        assert v == "Reilly"


def test_named_collection_decorator_affects_original_collection(surnames):
    original_surnames = surnames
    surnames = named_collection.NamedCollectionDecorator(surnames)
    surnames["Ignatius"] = "Reilly"
    assert original_surnames["Ignatius"] == "Reilly"


def test_named_collection_decorator_raise_key_error(surnames):
    surnames = named_collection.NamedCollectionDecorator(surnames)
    with pytest.raises(KeyError) as e:
        surnames["Ignatius"]
    assert "Ignatius" in str(e.value)


def test_check_subclass_decorator_correct_subclass(surnames):

    class TestClass(str):
        pass

    surnames = named_collection.CheckSubclassDecorator(surnames, str)
    surnames["Ignatius"] = TestClass
    assert len(surnames) == 1


def test_check_subclass_decorator_not_a_class(surnames):
    surnames = named_collection.CheckSubclassDecorator(surnames, str)
    with pytest.raises(TypeError) as e:
        surnames["Ignatius"] = "Reilly"
    assert "must be a class" in str(e.value)


def test_check_subclass_decorator_incorrect_subclass(surnames):

    class TestClass(str):
        pass

    surnames = named_collection.CheckSubclassDecorator(surnames, int)
    with pytest.raises(ValueError) as e:
        surnames["Ignatius"] = TestClass
    assert "Expecting class subclass of int" == str(e.value)


def test_check_instance_decorator_correct_instance(surnames):

    class SurnameClass(str):
        pass

    surnames = named_collection.CheckInstanceDecorator(surnames, str)
    surnames["Ignatius"] = SurnameClass()
    assert len(surnames) == 1


def test_check_instance_decorator_incorrect_instance(surnames):

    class SurnameClass(str):
        pass

    surnames = named_collection.CheckInstanceDecorator(surnames, int)
    with pytest.raises(ValueError) as e:
        surnames["Ignatius"] = SurnameClass()
    assert "Expecting instance of int" == str(e.value)


def test_suggestions_decorator(surnames):
    surnames = named_collection.SuggestionsDecorator(surnames)
    surnames["Ignatius"] = "Reilly"
    surnames["Ignacio"] = "Reilly"
    surnames["Myrna"] = "Minkoff"
    with pytest.raises(named_collection.KeyErrorWithSuggestions) as e:
        surnames["Ignatiu"]
    assert e.value.error_key == "Ignatiu"
    assert e.value.existing_keys == ["Ignatius", "Ignacio", "Myrna"]
    assert e.value.get_close_matches(n=1) == ["Ignatius"]
    assert e.value.get_close_matches() == ["Ignatius", "Ignacio"]
    assert "KeyError: 'Ignatiu'" in str(e.value)
    assert "Similar names: Ignatius, Ignacio" in str(e.value)


def test_suggestions_decorator_no_suggestions(surnames):
    surnames = named_collection.SuggestionsDecorator(surnames)
    with pytest.raises(named_collection.KeyErrorWithSuggestions) as e:
        surnames["Ignatius"]
    assert e.value.error_key == "Ignatius"
    assert e.value.existing_keys == []
    assert e.value.get_close_matches() == []
    assert "KeyError: 'Ignatius'" in str(e.value)


def test_suggestions_decorator_nested(surnames):
    surnames = named_collection.SuggestionsDecorator(surnames)
    surnames = named_collection.FailIfNameNoneDecorator(surnames)
    with pytest.raises(named_collection.KeyErrorWithSuggestions) as e:
        surnames["Ignatius"]
    assert e.value.error_key == "Ignatius"
    assert e.value.existing_keys == []
    assert e.value.get_close_matches() == []
    assert "KeyError: 'Ignatius'" in str(e.value)


def test_fail_if_name_none_decorator(surnames):
    surnames = named_collection.FailIfNameNoneDecorator(surnames)
    with pytest.raises(ValueError) as e:
        surnames[None] = "Reilly"
    assert "Name cannot be `None`" == str(e.value)


def test_fail_if_exists_decorator(surnames):
    surnames = named_collection.FailIfExistsDecorator(surnames)
    surnames["Ignatius"] = "Reilly"
    with pytest.raises(ValueError) as e:
        surnames["Ignatius"] = "Reilly"
    assert "Name 'Ignatius' already in use" == str(e.value)


def test_fail_if_exists_and_allow_update_decorators(surnames):
    original_surnames = surnames
    surnames = named_collection.FailIfExistsDecorator(surnames)
    surnames["Ignatius"] = "Reilly"
    surnames = named_collection.AllowUpdateDecorator(surnames)
    surnames["Ignatius"] = "Minkoff"
    assert original_surnames["Ignatius"] == "Minkoff"
