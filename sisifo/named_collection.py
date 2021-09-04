import collections
import difflib


class NamedCollection(collections.UserDict):
    def __missing__(self, key):  # pyrigth needs this because it's not defined in UserDict
        raise KeyError(key)


class BaseNamedCollection(NamedCollection):
    pass


class NamedCollectionDecorator(NamedCollection):
    data: NamedCollection  # pyrigth needs this because data is not an UserDict anymore

    def __init__(self, named_collection: NamedCollection):
        # Do not pass named_collection to super().__init__, it makes a copy.
        super().__init__()
        self.data = named_collection

    def __missing__(self, key):
        return self.data.__missing__(key)


class CheckSubclassDecorator(NamedCollectionDecorator):
    def __init__(self, named_collection, superclass):
        super().__init__(named_collection)
        self.superclass = superclass

    def __setitem__(self, name, element):
        if not issubclass(element, self.superclass):
            superclass_name = self.superclass.__name__
            raise ValueError(f"Expecting class subclass of {superclass_name}")
        super().__setitem__(name, element)


class CheckInstanceDecorator(NamedCollectionDecorator):
    def __init__(self, named_collection, superclass):
        super().__init__(named_collection)
        self.superclass = superclass

    def __setitem__(self, name, element):
        if not isinstance(element, self.superclass):
            superclass_name = self.superclass.__name__
            raise ValueError(f"Expecting instance of {superclass_name}")
        super().__setitem__(name, element)


class KeyErrorWithSuggestions(KeyError):
    def __init__(self, error_key, existing_keys):
        self.error_key = error_key
        self.existing_keys = existing_keys
        super().__init__(self._create_message())

    def _create_message(self):
        message = f"KeyError: '{self.error_key}'"
        matches = self.get_close_matches()
        if len(matches):
            message += f". Similar names: {', '.join(matches)}"
        return message

    def get_close_matches(self, n=3):
        return difflib.get_close_matches(self.error_key, self.existing_keys, n=n)


class SuggestionsDecorator(NamedCollectionDecorator):
    def __missing__(self, name):
        raise KeyErrorWithSuggestions(name, list(self.keys()))


class FailIfNameNoneDecorator(NamedCollectionDecorator):
    def __setitem__(self, name, element):
        if name is None:
            raise ValueError("Name cannot be `None`")
        super().__setitem__(name, element)


class FailIfExistsDecorator(NamedCollectionDecorator):
    def __setitem__(self, name, element):
        if name in self:
            raise ValueError(f"Name '{name}' already in use")
        super().__setitem__(name, element)


class AllowUpdateDecorator(NamedCollectionDecorator):
    def __setitem__(self, name, element):
        if name in self:
            del self[name]
        super().__setitem__(name, element)


class NamedCollectionBuilder:
    def __init__(self):
        self._collection = BaseNamedCollection()

    def subclass_of(self, subclass):
        self._collection = CheckSubclassDecorator(self._collection, subclass)
        return self

    def instance_of(self, class_):
        self._collection = CheckInstanceDecorator(self._collection, class_)
        return self

    def suggestions(self):
        self._collection = SuggestionsDecorator(self._collection)
        return self

    def fail_if_name_none(self):
        self._collection = FailIfNameNoneDecorator(self._collection)
        return self

    def fail_if_exists(self):
        self._collection = FailIfExistsDecorator(self._collection)
        return self

    def build(self):
        return self._collection
