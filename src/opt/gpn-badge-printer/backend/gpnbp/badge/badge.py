from __future__ import absolute_import

from PIL import Image, ImageDraw
import logging
from gpnbp.configuration import GPNBPConfig


class BadgeGenerator:
    def __init__(self, config: GPNBPConfig.Badge):
        self.size = config.size
        logging.info(f'Badge size: ({self.size.width}x{self.size.height})')

        if config.preview.background is not None:
            logging.debug(f'Loading Background image: {config.preview.background}')
            self.badge_background = Image.open(config.preview.background)
        else:
            logging.info(f'No Background Image set')
            self.badge_background = None

        self.fields = dict()
        for field in config.fields:
            logging.debug(f'Initializing Textfield: {field}')
            self.fields[field] = TextField(self, config.fields[field])

    def getBadge(self, strings: dict[str, str], show_background: bool = False, show_margins: bool = False) -> Image:
        logging.info(f'Generating Badge: {strings}, {show_background}')
        image = Image.new("RGBA", (self.size.width, self.size.height))
        draw = ImageDraw.Draw(image)
        if show_background:
            image.paste(self.badge_background)

        for (key, value) in strings.items():
            self.fields[key].draw(draw, value, show_margins)
        return image


from gpnbp.badge.textfield import TextField
