import abc
import json

try:
    import yaml
    yaml_exists = True
except ImportError:
    yaml_exists = False


class Configuration(abc.ABC):
    @abc.abstractmethod
    def get_config_dictionary(self):
        pass


class DictionaryConfiguration(Configuration):
    def __init__(self, config):
        self.config = config

    def get_config_dictionary(self):
        return self.config


class TextSourceStrategy(abc.ABC):
    @abc.abstractmethod
    def get_text(self):
        pass


class StringTextSourceStrategy(TextSourceStrategy):
    def __init__(self, string):
        self.string = string

    def get_text(self):
        return self.string


class FileTextSourceStrategy(TextSourceStrategy):
    def __init__(self, filename):
        self.filename = filename

    def get_text(self):
        with open(self.filename) as file:
            return file.read()


class TextFormatStrategy(abc.ABC):
    @abc.abstractmethod
    def to_dict(self, text):
        pass


class JSONTextFormatStrategy(TextFormatStrategy):
    def to_dict(self, text):
        return json.loads(text)


class YAMLTextFormatStrategy(TextFormatStrategy):
    def to_dict(self, text):
        self.check_pyyaml_installed()
        # If we use "yaml" here and yaml is not installed we will get a NameError.
        return self.load(text)

    def load(self, text):
        return yaml.safe_load(text)

    def check_pyyaml_installed(self):
        if not yaml_exists:
            raise ImportError("Install pyyaml package to use YAML config files")


class TextConfiguration(Configuration):
    def __init__(self, source_strategy, format_strategy):
        self.source_strategy = source_strategy
        self.format_strategy = format_strategy

    def get_config_dictionary(self):
        text = self.source_strategy.get_text()
        data = self.format_strategy.to_dict(text)
        return data


# TODO: implement SQL database configuration reader.
class SQLDatabaseConfiguration(Configuration):
    pass


FORMATS = {
    "json": JSONTextFormatStrategy,
    "yaml": YAMLTextFormatStrategy,
}

SOURCES = {
    "string": StringTextSourceStrategy,
    "file": FileTextSourceStrategy,
}


def from_text(text_or_filename, origin="file", format="json"):
    if type(origin) == str:
        origin = SOURCES[origin](text_or_filename)
    if type(format) == str:
        format = FORMATS[format]()
    conf = TextConfiguration(origin, format).get_config_dictionary()
    return conf
