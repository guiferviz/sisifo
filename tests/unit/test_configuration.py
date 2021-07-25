from sisifo.configuration import JSONTextFormatStrategy
from sisifo.configuration import StringTextSourceStrategy
from sisifo.configuration import TextConfiguration
from sisifo.configuration import TextFormatStrategy
from sisifo.configuration import YAMLTextFormatStrategy


YAML_TEXT = """
name: Ignatius J. Reilly
likes:
 - theology
 - geometry
 - scholastic philosophy
"""
JSON_TEXT = """
{
    "name": "Ignatius J. Reilly",
    "likes": ["theology", "geometry", "scholastic philosophy"]
}
"""
EXPECTED_CONFIGURATION = {
    "name": "Ignatius J. Reilly",
    "likes": ["theology", "geometry", "scholastic philosophy"],
}


class MockTextFormatStrategy(TextFormatStrategy):
    def to_dict(self, text):
        return text


def test_string_text_source_strategy():
    expected = "dunce"
    source = StringTextSourceStrategy(expected)
    current = source.get_text()
    assert current == expected


def test_json_text_format_strategy():
    format_ = JSONTextFormatStrategy()
    current = format_.to_dict(JSON_TEXT)
    assert current == EXPECTED_CONFIGURATION


def test_yaml_text_format_strategy():
    format_ = YAMLTextFormatStrategy()
    current = format_.to_dict(YAML_TEXT)
    assert current == EXPECTED_CONFIGURATION


def test_text_configuration():
    expected = "dunce"
    source = StringTextSourceStrategy(expected)
    format_ = MockTextFormatStrategy()
    conf = TextConfiguration(source, format_)
    current = conf.get_config_dictionary()
    assert current == expected
