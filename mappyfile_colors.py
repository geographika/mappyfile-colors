from mappyfile.transformer import MapfileTransformer, MapfileToDict
from mappyfile.parser import Parser
import webcolors
from lark.lexer import Token

__version__ = "0.1.0"


class ConversionType:
    NO_CONVERSION = 0
    TO_RGB = 1
    TO_HEX = 2


def token_to_rgb(t):
    r, g, b = t
    return (r.value, g.value, b.value)


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
            # print(webcolors.rgb_to_name(t)) # TODO - add this as a comment to the tree
            return Token("HEXCOLOR", hex)

    def colorrange(self, t):

        if self.conversion_type == ConversionType.TO_RGB:
            return super(ColoursTransformer, self).colorrange(t)
        else:
            t1 = t[:3]
            t2 = t[3:]
            hex1 = webcolors.rgb_to_hex(token_to_rgb(t1))
            hex2 = webcolors.rgb_to_hex(token_to_rgb(t2))
            return [Token("HEXCOLOR", hex1), Token("HEXCOLOR", hex2)]

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
                      transformerClass=ColoursTransformer, conversion_type=conversion_type)
    d = m.transform(ast)
    return d
