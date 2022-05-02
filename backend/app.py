import json
import tempfile
from gpnbd.printer import Printer
from gpnbd.pretix import PretixAPI
from gpnbd.badge import BadgeGenerator
import gpnbd.exceptions
from pathlib import Path
import hashlib

# Load config
try:
    with open('conf.json') as f:
        config = json.loads(f.read())
        printer = Printer(config['cups']['printer'])
        badge = BadgeGenerator(config=config['badge'], show_margins=config['app']['debug'])
        pretix = PretixAPI(url=config['pretix']['url'],
                           event=config['pretix']['event'],
                           token=config['pretix']['token'])
except (OSError, KeyError, json.JSONDecodeError):
    raise gpnbd.exceptions.ConfigurationError("Couldn't load configuration")

name_string = "GADSE"

badge_file = badge.getBadge(name_string)
badge_file.show()
file = (Path('/tmp/') / hashlib.md5(name_string.encode()).hexdigest())
badge_file.save(file.as_posix(), format='png')
printer.printFile(file)
