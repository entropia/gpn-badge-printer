from PIL import Image, ImageDraw, ImageFont, ImageColor


class ImageSize(tuple[int, int]):
    @property
    def width(self):
        return self[0]

    @property
    def height(self):
        return self[1]


class ImageMargins(tuple[int, int, int, int]):
    @property
    def left(self):
        return self[0]

    @property
    def right(self):
        return self[1]

    @property
    def top(self):
        return self[2]

    @property
    def bottom(self):
        return self[3]


class BadgeGenerator:
    def __init__(self, config, show_margins=False):
        self.size = ImageSize([config['size']['width'], config['size']['height']])
        self.show_margins = show_margins
        self.bage_backound = Image.open(config['preview']['background'])
        self.fields = dict()
        for field in config['fields']:
            self.fields[field] = TextField(self, config['fields'][field])

    def getBadge(self, strings: dict[str, str], show_background: bool) -> Image:
        image = Image.new("RGBA", self.size)
        draw = ImageDraw.Draw(image)
        if show_background:
            image.paste(self.bage_backound)

        for (key, value) in strings.items():
            self.fields[key].draw(draw, value)
        return image


class TextField:
    def __init__(self, parent: BadgeGenerator, config: dict):
        self.parent = parent
        self.font_path = config['font']['path']
        self.font_size = config['font']['size']
        self.margins = ImageMargins([config['margins']['left'], config['margins']['right'], config['margins']['top'],
                                     config['margins']['bottom']])
        self.debug = config['debug']

        if config['text']['position'] is not None:
            self.text_position = (config['text']['position']['x'], config['text']['position']['y'])
        else:
            x = int((parent.size.width - self.margins.left - self.margins.right) / 2 + self.margins.left)
            y = int((parent.size.height - self.margins.top - self.margins.bottom) / 2 + self.margins.top)
            self.text_position = (x, y)
        print(self.text_position)
        self.text_anchor = config['text']['anchor']

    def draw(self, draw: ImageDraw.Draw, string: str):
        if self.parent.show_margins:
            # Left
            draw.line([(self.margins.left, 0), (self.margins.left, self.parent.size.height)],
                      fill=self.debug['color'],
                      width=self.debug['width'])
            # Right
            draw.line(
                [(self.parent.size.width - self.margins.right, 0),
                 (self.parent.size.width - self.margins.right, self.parent.size.height)],
                fill=self.debug['color'],
                width=self.debug['width'])
            # Top
            draw.line([(0, self.margins.top), (self.parent.size.width, self.margins.top)],
                      fill=self.debug['color'],
                      width=self.debug['width'])
            # Bottom
            draw.line([(0, self.parent.size.height - self.margins.bottom),
                       (self.parent.size.width, self.parent.size.height - self.margins.bottom)],
                      fill=self.debug['color'],
                      width=self.debug['width'])

        # Reduce text size
        font_size = self.font_size
        font = ImageFont.truetype(self.font_path, font_size)
        text_width, text_height = draw.textsize(string, font=font)
        while text_height > self.parent.size.height - self.margins.top - self.margins.bottom:
            font_size = font_size - 1
            font = ImageFont.truetype(self.font_path, font_size)
            text_width, text_height = draw.textsize(string, font=font)
        print(f'Reduced font size to {font_size}')

        # Reduce text length
        text_width, text_height = draw.textsize(string, font=font)
        while text_width > self.parent.size.width - self.margins.left - self.margins.right:
            string = string[:-1]
            text_width, text_height = draw.textsize(string, font=font)

        # Draw Text
        draw.text(self.text_position, string, fill=(0, 0, 0, 255), anchor=self.text_anchor, font=font)
