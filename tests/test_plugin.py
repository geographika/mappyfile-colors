import pytest
import mappyfile
import mappyfile_colors
from mappyfile.plugins import mappyfile_colors 
from mappyfile_colors import ColoursTransformer, ConversionType
from mappyfile.parser import Parser
from mappyfile.transformer import MapfileToDict, MapfileTransformer
from mappyfile.pprint import PrettyPrinter


def test_simple_api():

    s = """
    CLASS
        STYLE
            COLOR 184 134 11
            OUTLINECOLOR 0 0 255
            WIDTH 3
        END
    END
    """

    d = mappyfile.loads(s, include_comments=True, transformerClass=ColoursTransformer, conversion_type=ConversionType.TO_HEX)
    output = mappyfile.dumps(d, indent=0, newlinechar=" ")
    assert output == 'CLASS STYLE COLOR "#b8860b" # darkgoldenrod OUTLINECOLOR "#0000ff" # blue WIDTH 3 END END'


def test_simple_api_rgb():

    s = """
    CLASS
        STYLE
            COLOR "#b8860b"
            OUTLINECOLOR "#0000ff"
            WIDTH 3
        END
    END
    """

    d = mappyfile.loads(s, include_comments=True, transformerClass=ColoursTransformer, conversion_type=ConversionType.TO_RGB)
    output = mappyfile.dumps(d, indent=0, newlinechar=" ")
    print(output)
    assert output == 'CLASS STYLE COLOR 184 134 11 # darkgoldenrod OUTLINECOLOR 0 0 255 # blue WIDTH 3 END END'


def test_api():

    s = """
    CLASS
        STYLE
            COLOR 184 134 11
            OUTLINECOLOR 0 0 255
            WIDTH 3
        END
    END
    """

    p = Parser(expand_includes=True, include_comments=True)
    ast = p.parse(s)

    m = MapfileToDict(include_comments=True,
                      transformerClass=ColoursTransformer,
                      conversion_type=ConversionType.TO_HEX)

    d = m.transform(ast)
    pp = PrettyPrinter(indent=0, newlinechar=" ")
    output = pp.pprint(d)
    assert output == 'CLASS STYLE COLOR "#b8860b" # darkgoldenrod OUTLINECOLOR "#0000ff" # blue WIDTH 3 END END'


def run_tests():
    pytest.main(["tests/test_plugin.py", "-vv"])


if __name__ == '__main__':
    test_simple_api_rgb()
    # run_tests()
    print("Done!")
