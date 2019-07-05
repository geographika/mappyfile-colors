import itertools
from mappyfile.transformer import MapfileTransformer, CommentsTransformer, MapfileToDict
from mappyfile.parser import Parser
from lark.visitors import v_args
import webcolors
from lark.lexer import Token

__version__ = "0.4.0"


class ConversionType:
    NO_CONVERSION = 0
    TO_RGB = 1
    TO_HEX = 2


class ColorToken(Token):
    """
    A token subclass with an additional comment attribute
    to store the color name so it can be accessed
    by the transformer
    """
    __slots__ = 'comment'


def token_to_rgb(t):
    r, g, b = t
    return (r.value, g.value, b.value)


def rgb_to_hex_token(rgb, include_color_names):

    hex = webcolors.rgb_to_hex(rgb)
    return hex_to_token(hex, include_color_names)


def hex_to_rgb_token(hex, include_color_names):

    rgb = webcolors.hex_to_rgb(hex)
    return rgb_to_token(rgb, include_color_names)


def rgb_to_token(rgb, include_color_names):

    r, g, b = rgb
    rgb_token = ColorToken("RGB", [r, g, b])
    if include_color_names:
        add_token_comment(rgb_token)
    return rgb_token


def hex_to_token(hex, include_color_names):

    hex_token = ColorToken("HEXCOLOR", hex)
    if include_color_names:
        add_token_comment(hex_token)
    return hex_token


def hex_to_name(hex):

    try:
        name = webcolors.hex_to_name(hex)
    except ValueError:
        name = "unnamed"
    return name


def add_token_comment(token):

    if token.type == "RGB":
        hex = webcolors.rgb_to_hex(token.value)
    else:
        assert token.type == "HEXCOLOR"
        hex = token.value

    token.comment = hex_to_name(hex)
    return token


orig_function = CommentsTransformer._save_attr_comments


@v_args(tree=True)
def attr_comments_override(self, tree):
    """
    Override the standard comments function to check for any ColorTokens and
    add the human named colors to the comments array associated with the color
    """

    d = orig_function(self, tree)
    if "__tokens__" in d:
        for t in d["__tokens__"]:
            if isinstance(t, ColorToken) and hasattr(t, "comment"):
                # append the comment to the comments list if not already present
                # this could happen if the Mapfile is parsed several times
                comment = "# {}".format(t.comment)
                if comment not in d["__comments__"]:
                    d["__comments__"] += [comment]

    return d


CommentsTransformer.attr = attr_comments_override


class ColorsTransformer(MapfileTransformer):
    """
    A custom transformer that can convert from RGB to HEX color
    formats, and add in the color name as a comment
    """
    def __init__(self, include_position=False, include_comments=False,
                 conversion_type=ConversionType.TO_RGB, include_color_names=False):

        self.conversion_type = conversion_type

        if include_color_names is True:
            include_comments = True

        self.include_color_names = include_color_names

        super(ColorsTransformer, self).__init__(include_position, include_comments)

    def rgb(self, t):
        """
        Convert rgb values to hex if appropriate, if not
        return the standard transformation
        """

        rgb = token_to_rgb(t)

        if self.conversion_type == ConversionType.TO_HEX:
            hex_token = rgb_to_hex_token(rgb, self.include_color_names)
            return hex_token
        else:
            return rgb_to_token(rgb, self.include_color_names)

    def hexcolor(self, t):
        """
        Convert hex values to rgb if appropriate, if not
        return the standard transformation
        """

        hex = self.clean_string(t[0])

        if self.conversion_type == ConversionType.TO_RGB:
            rgb_token = hex_to_rgb_token(hex, self.include_color_names)
            return rgb_token
        else:
            return hex_to_token(hex, self.include_color_names)

    def colorrange(self, t):
        """
        Convert a rgb colorange to a hex colorrange

        Input is [Token(SIGNED_INT, 0), Token(SIGNED_INT, 0), Token(SIGNED_INT, 0),
        Token(SIGNED_INT, 255), Token(SIGNED_INT, 255), Token(SIGNED_INT, 255)]
        """

        if self.conversion_type == ConversionType.TO_RGB:
            return super(ColorsTransformer, self).colorrange(t)
        else:
            t1 = t[:3]
            t2 = t[3:]
            hex_token1 = rgb_to_hex_token(token_to_rgb(t1), self.include_color_names)
            hex_token2 = rgb_to_hex_token(token_to_rgb(t2), self.include_color_names)
            return [hex_token1, hex_token2]

    def hexcolorrange(self, t):
        """
        Convert a hex colorange to a rgb colorrange
        """

        if self.conversion_type == ConversionType.TO_RGB:
            r1, g1, b1 = t[0].value  # t[0].comment
            r2, g2, b2 = t[1].value

            # TODO why can't 2 RGB values simply be returned here?

            # Input is [Token(RGB, [0, 0, 0]), Token(RGB, [255, 255, 255])]

            # colorrange rule expects [Token(SIGNED_INT, 0), Token(SIGNED_INT, 0), Token(SIGNED_INT, 0),
            # Token(SIGNED_INT, 255), Token(SIGNED_INT, 255), Token(SIGNED_INT, 0)]

            return [Token("SIGNED_INT", r1), Token("SIGNED_INT", g1), Token("SIGNED_INT", b1),
                    Token("SIGNED_INT", r2), Token("SIGNED_INT", g2), Token("SIGNED_INT", b2)]
        else:
            return super(ColorsTransformer, self).hexcolorrange(t)


def colors_transform(s, conversion_type=ConversionType.NO_CONVERSION, include_comments=False,
                     include_color_names=False):
    """
    Parse the string with a custom colors transformer
    """

    p = Parser(include_comments=include_comments)
    ast = p.parse(s)

    if include_color_names:
        include_comments = True

    m = MapfileToDict(include_comments=include_comments,
                      transformerClass=ColorsTransformer,
                      conversion_type=conversion_type,
                      include_color_names=include_color_names)

    d = m.transform(ast)

    return d


class ColorFactory:

    palettes = {
        # http://artshacker.com/wp-content/uploads/2014/12/Kellys-22-colour-chart.jpg
        "maximum_contrast": ['#e6194b', '#3cb44b', '#ffe119', '#4363d8',
                             '#f58231', '#911eb4', '#46f0f0', '#f032e6',
                             '#bcf60c', '#fabebe', '#008080', '#e6beff',
                             '#9a6324', '#fffac8', '#800000', '#aaffc3',
                             '#808000', '#ffd8b1', '#000075', '#808080',
                             '#ffffff', '#000000']
    }

    def get_colors(self, palette_name=None, repeat=False):

        if palette_name is None:
            palette_name = "maximum_contrast"

        palette_name = palette_name.lower()
        colours = self.palettes[palette_name]

        if repeat:
            colours = itertools.cycle(colours)

        for clr in colours:
            yield clr

    @property
    def palette_names(self):
        """
        A list of all palette names available in the factory
        """
        return sorted(self.palettes.keys())
