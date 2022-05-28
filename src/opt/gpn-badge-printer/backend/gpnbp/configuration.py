from typing import Union, Sequence, Any
from pathlib import Path
import json


class ConfigurationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ConfigOption:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class GPNBPConfig(ConfigOption):
    class Badge(ConfigOption):
        class Size(ConfigOption):
            width: int
            height: int

        class Preview(ConfigOption):
            background: Union[str, Path, None] = None
            # TODO: Move to API request
            showMargins: bool = False

        class Textfield(ConfigOption):
            class Text(ConfigOption):
                anchor: str = 'mm'
                position: Union[None, tuple[int, int]] = None

            class Font(ConfigOption):
                path: Union[str, Path]
                max_size: int
                min_size: int

            class Margins(ConfigOption):
                left: int
                right: int
                top: int
                bottom: int

            class Debug(ConfigOption):
                color: Union[str, tuple[int, int, int]]
                width: int = 2

            text: Text
            font: Font
            margins: Margins
            debug: Debug
            description: str = ''
            max_length: int = 0

            def __init__(self, **kwargs):
                self.text = self.Text(**kwargs['text'])
                self.font = self.Font(**kwargs['font'])
                self.margins = self.Margins(**kwargs['margins'])
                self.debug = self.Debug(**kwargs['debug'])
                self.description = kwargs['description']

        size: Size
        preview: Preview
        fields: dict[str, Textfield]

        def __init__(self, **kwargs):
            self.size = self.Size(**kwargs['size'])
            self.preview = self.Preview(**kwargs['preview'])
            self.fields = dict()
            for field in kwargs['fields']:
                self.fields[field] = self.Textfield(**kwargs['fields'][field])

    class App(ConfigOption):
        host: str = '127.0.0.1'
        port: int = 8000
        debug: bool = False
        log_level: str = 'INFO'

    class Cups(ConfigOption):
        printer_name: str
        enabled: bool

    class Ticket(ConfigOption):
        class Datasource(ConfigOption):
            name: str
            config: dict[str, Any]

        datasource: Datasource
        enabled: bool

        def __init__(self, **kwargs):
            self.enabled = kwargs['enabled']
            if self.enabled:
                self.datasource = self.Datasource(**kwargs['data_source'])

    app: App
    cups: Cups
    badge: Badge
    ticket: Ticket

    def __init__(self, file: Union[str, Path]):
        try:
            with open(file) as f:
                config = json.loads(f.read())
            self.app = GPNBPConfig.App(**config['app'])
            self.cups = GPNBPConfig.Cups(**config['cups'])
            self.badge = GPNBPConfig.Badge(**config['badge'])
            self.ticket = GPNBPConfig.Ticket(**config['ticket'])
        except (OSError, KeyError, json.JSONDecodeError) as e:
            raise ConfigurationError(e)
