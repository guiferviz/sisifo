from sisifo.named_collection import NamedCollectionBuilder
from sisifo.named_collection import NamedCollectionDecorator


class DataCollection(NamedCollectionDecorator):
    def __init__(self):
        data = (
            NamedCollectionBuilder()
            .suggestions()
            .build()
        )
        super().__init__(data)
