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


orig_function = CommentsTransformer._save_attr_comments


@v_args(tree=True)
def attr_comments_override(self, tree):
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
            hex = webcolors.rgb_to_hex(token_to_rgb(t))
            named_colour = webcolors.hex_to_name(hex)
            converted_token = ColorToken("HEXCOLOR", hex)
            converted_token.comment = named_colour
            return converted_token

    def colorrange(self, t):

        if self.conversion_type == ConversionType.TO_RGB:
            return super(ColoursTransformer, self).colorrange(t)
        else:
            t1 = t[:3]
            t2 = t[3:]
            hex1 = webcolors.rgb_to_hex(token_to_rgb(t1))
            hex2 = webcolors.rgb_to_hex(token_to_rgb(t2))
            hex_token1 = ColorToken("HEXCOLOR", hex1)
            hex_token1.comment = webcolors.hex_to_name(hex1)
            hex_token2 = ColorToken("HEXCOLOR", hex2)
            hex_token2.comment = webcolors.hex_to_name(hex2)
            return [hex_token1, hex_token2]

    def hexcolorrange(self, t):

        if self.conversion_type == ConversionType.TO_RGB:
            r1, g1, b1 = t[0].value
            r2, g2, b2 = t[1].value
            return [Token("SIGNED_INT", r1), Token("SIGNED_INT", g1), Token("SIGNED_INT", b1),
                    Token("SIGNED_INT", r2), Token("SIGNED_INT", g2), Token("SIGNED_INT", b2)]
        else:
            return super(ColoursTransformer, self).hexcolorrange(t)

    def hexcolor(self, t):

        if self.conversion_type == ConversionType.TO_RGB:
            r, g, b = webcolors.hex_to_rgb(self.clean_string(t[0]))
            return Token("RGB", [r, g, b])
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
