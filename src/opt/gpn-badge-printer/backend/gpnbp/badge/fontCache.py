from typing import Union
from pathlib import Path
from PIL import ImageFont
import logging


class FontCache:
    min_size: int
    max_size: int
    font_path: Union[str, Path]

    cache: dict[int, ImageFont]

    def __init__(self,
                 font_path: Union[str, Path],
                 min_size: int,
                 max_size: int):
        self.font_path = font_path
        self.min_size = min_size
        self.max_size = max_size

        logging.info(f'Initilising font cache \'{font_path}\': {min_size}-{max_size}')

        self.cache = dict()
        for font_size in range(min_size, max_size+1):
            self.cache[font_size] = ImageFont.truetype(self.font_path, font_size)
