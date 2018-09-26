from mappyfile.transformer import MapfileTransformer, CommentsTransformer, MapfileToDict
from mappyfile.parser import Parser
from lark.visitors import v_args
import webcolors
from lark.lexer import Token

__version__ = "0.1.0"


class ConversionType:
    NO_CONVERSION = 0
    TO_RGB = 1
    TO_HEX = 2


class ColorToken(Token):
    __slots__ = 'comment'


def token_to_rgb(t):
    r, g, b = t
    return (r.value, g.value, b.value)


def rgb_to_hex_token(rgb):
    hex = webcolors.rgb_to_hex(rgb)
    hex_token = ColorToken("HEXCOLOR", hex)
    add_token_comment(hex_token)
    return hex_token


def hex_to_rgb_token(hex):

    rgb = webcolors.hex_to_rgb(hex)
    return rgb_to_token(rgb)


def rgb_to_token(rgb):

    r, g, b = rgb
    rgb_token = ColorToken("RGB", [r, g, b])
    add_token_comment(rgb_token)
    return rgb_token


def add_token_comment(token):

    if token.type == "RGB":
        hex = webcolors.rgb_to_hex(token.value)
    else:
        assert token.type == "HEXCOLOR"
        hex = token.value

    try:
        token.comment = webcolors.hex_to_name(hex)
    except ValueError:
        token.comment = "No color name found"

orig_function = CommentsTransformer._save_attr_comments


@v_args(tree=True)
def attr_comments_override(self, tree):
    """
    Override the standard comments function to check for any ColorTokens and
    add the human named colours to the comments array associated with the colour
    """
    d = orig_function(self, tree)
    if "__tokens__" in d:
        for t in d["__tokens__"]:
            if isinstance(t, ColorToken):
                d["__comments__"] += ["# {}".format(t.comment)]
    return d


CommentsTransformer.attr = attr_comments_override


class ColoursTransformer(MapfileTransformer):

    def __init__(self, include_position=False, include_comments=False,
                 conversion_type=ConversionType.TO_RGB):

        self.conversion_type = conversion_type
        super(ColoursTransformer, self).__init__(include_position, include_comments)

    def rgb(self, t):

        if self.conversion_type == ConversionType.TO_RGB:
            return super(ColoursTransformer, self).rgb(t)
        else:
            hex_token = rgb_to_hex_token(token_to_rgb(t))
            return hex_token

    def colorrange(self, t):

        if self.conversion_type == ConversionType.TO_RGB:
            return super(ColoursTransformer, self).colorrange(t)
        else:
            t1 = t[:3]
            t2 = t[3:]
            hex_token1 = rgb_to_hex_token(token_to_rgb(t1))
            hex_token2 = rgb_to_hex_token(token_to_rgb(t2))
            return [hex_token1, hex_token2]

    def hexcolorrange(self, t):

        if self.conversion_type == ConversionType.TO_RGB:
            #return [Token("SIGNED_INT", r1), Token("SIGNED_INT", g1), Token("SIGNED_INT", b1),
            #        Token("SIGNED_INT", r2), Token("SIGNED_INT", g2), Token("SIGNED_INT", b2)]
            #rgb_token1 = rgb_to_token(t[0].value)
            #rgb_token2 = rgb_to_token(t[1].value)
            #return [rgb_token1, rgb_token2]
            print(t)
            #return [t[0].value, t[1].value]
            r1, g1, b1 = t[0].value
            r2, g2, b2 = t[1].value
            vals =  [Token("SIGNED_INT", r1), Token("SIGNED_INT", g1), Token("SIGNED_INT", b1),
                       Token("SIGNED_INT", r2), Token("SIGNED_INT", g2), Token("SIGNED_INT", b2)]

            token = ColorToken("COLORRANGE")
            return [ColorToken("COLORRANGE"), Token("SIGNED_INT", r1), Token("SIGNED_INT", g1), Token("SIGNED_INT", b1),
                       Token("SIGNED_INT", r2), Token("SIGNED_INT", g2), Token("SIGNED_INT", b2)]
        else:
            return super(ColoursTransformer, self).hexcolorrange(t)

    def hexcolor(self, t):

        if self.conversion_type == ConversionType.TO_RGB:
            hex = self.clean_string(t[0])
            rgb_token = hex_to_rgb_token(hex)
            return rgb_token
        else:
            return super(ColoursTransformer, self).hexcolor(t)


def colours_transform(s, conversion_type=ConversionType.NO_CONVERSION, include_comments=False):
    p = Parser(include_comments=include_comments)
    ast = p.parse(s)

    m = MapfileToDict(include_comments=include_comments,
                      transformerClass=ColoursTransformer,
                      conversion_type=conversion_type)
    d = m.transform(ast)
    return d
