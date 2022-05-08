from PIL import ImageDraw, ImageFont
import logging

from gpnbp.badge.badge import BadgeGenerator
from gpnbp.configuration import GPNBPConfig
from gpnbp.badge.fontCache import FontCache


class TextField:
    font_cache: FontCache
    margins: GPNBPConfig.Badge.Textfield.Margins
    debug: GPNBPConfig.Badge.Textfield.Debug

    def __init__(self, parent: BadgeGenerator, config: GPNBPConfig.Badge.Textfield):
        self.parent = parent
        self.font_cache = FontCache(font_path=config.font.path,
                                    max_size=config.font.max_size,
                                    min_size=config.font.min_size)
        self.margins = config.margins
        self.debug = config.debug

        # TODO: When picking the text position automatically the text anchor should be used
        if config.text.position is not None:
            self.text_position = (config.text.position[0], config.text.position[1])
        else:
            x = int((parent.size.width - self.margins.left - self.margins.right) / 2 + self.margins.left)
            y = int((parent.size.height - self.margins.top - self.margins.bottom) / 2 + self.margins.top)
            self.text_position = (x, y)
        self.text_anchor = config.text.anchor

        logging.debug(f'Text postion is ({self.text_anchor}) x: {self.text_position[0]}, y: {self.text_position[1]}')

    def draw(self, draw: ImageDraw.Draw, string: str, show_margins: bool):
        if show_margins:
            # Left
            draw.line([(self.margins.left, 0),
                       (self.margins.left, self.parent.size.height)],
                      fill=self.debug.color,
                      width=self.debug.width)
            # Right
            draw.line([(self.parent.size.width - self.margins.right, 0),
                       (self.parent.size.width - self.margins.right, self.parent.size.height)],
                      fill=self.debug.color,
                      width=self.debug.width)
            # Top
            draw.line([(0, self.margins.top),
                       (self.parent.size.width, self.margins.top)],
                      fill=self.debug.color,
                      width=self.debug.width)
            # Bottom
            draw.line([(0, self.parent.size.height - self.margins.bottom),
                       (self.parent.size.width, self.parent.size.height - self.margins.bottom)],
                      fill=self.debug.color,
                      width=self.debug.width)

        # Reduce text size
        size = self.font_cache.max_size
        text_width, text_height = draw.textsize(string, font=self.font_cache.cache[size])
        while text_height > self.parent.size.height - self.margins.top - self.margins.bottom or text_width > self.parent.size.width - self.margins.left - self.margins.right:
            size = size - 1
            text_width, text_height = draw.textsize(string, font=self.font_cache.cache[size])
            if size == self.font_cache.min_size:
                break
        logging.debug(f'Reduced font size to {size}')

        # Reduce text length
        text_width, text_height = draw.textsize(string, font=self.font_cache.cache[size])
        while text_width > self.parent.size.width - self.margins.left - self.margins.right:
            string = string[:-1]
            text_width, text_height = draw.textsize(string, font=self.font_cache.cache[size])

        # Draw Text
        draw.text(self.text_position, string, fill=(0, 0, 0, 255), anchor=self.text_anchor,
                  font=self.font_cache.cache[size])
