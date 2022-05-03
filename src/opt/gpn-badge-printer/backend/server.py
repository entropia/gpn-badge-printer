import json
import tempfile
from gpnbp.printer import Printer
from gpnbp.pretix import PretixAPI
from gpnbp.badge import BadgeGenerator
import gpnbp.exceptions
from pathlib import Path
import hashlib

# Load config
try:
    with open('files/conf.json') as f:
        config = json.loads(f.read())
        printer = Printer(config['cups']['printer'])
        badge = BadgeGenerator(config=config['badge'], show_margins=config['app']['debug'])
        pretix = PretixAPI(url=config['pretix']['url'],
                           event=config['pretix']['event'],
                           token=config['pretix']['token'])
except (OSError, KeyError, json.JSONDecodeError):
    raise gpnbp.exceptions.ConfigurationError("Couldn't load configuration")

name_string = "1234567890123456789012345678901234567890123456789012345678901234567890"
badge_file = badge.getBadge(name_string)
badge_file.show()
file = (Path('/tmp/') / hashlib.md5(name_string.encode()).hexdigest())
badge_file.save(file.as_posix(), format='png')

if config['cups']['enable']:
    printer.printFile(file)

