import json
import mappyfile_colors
import pytest
from mappyfile_colors import ConversionType
from mappyfile.pprint import PrettyPrinter


def test_to_rgb():
    s = """
    STYLE
        COLOR "#ff0000"
        OUTLINECOLOR "#00ff00"
        COLORRANGE "#000000" "#ffffff"
    END
    """

    d = mappyfile_colors.colours_transform(s, ConversionType.TO_RGB)
    print(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    exp = "STYLE COLOR 255 0 0 OUTLINECOLOR 0 255 0 COLORRANGE 0 0 0 255 255 255 END"
    assert s == exp


def test_to_hex():
    s = """
    STYLE
        COLOR 255 0 0
        OUTLINECOLOR 0 255 0
        COLORRANGE 0 0 0 255 255 255
    END
    """

    d = mappyfile_colors.colours_transform(s, ConversionType.TO_HEX)
    # print(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    # print(s)
    exp = "STYLE COLOR '#ff0000' OUTLINECOLOR '#00ff00' COLORRANGE '#000000' '#ffffff' END"
    assert s == exp


def test_add_comments():
    s = """
    STYLE
        COLOR 255 0 0 # red
        OUTLINECOLOR 0 255 0
        COLORRANGE 0 0 0 255 255 255
    END
    """

    d = mappyfile_colors.colours_transform(s, ConversionType.TO_HEX, include_comments=True)
    jsn = json.dumps(d, indent=4)
    print(jsn)
    assert d["__comments__"]["color"][0] == "# red"
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    print(s)
    exp = """STYLE
COLOR '#ff0000' # red
OUTLINECOLOR '#00ff00'
COLORRANGE '#000000' '#ffffff'
END"""

    assert s == exp


def run_tests():
    pytest.main(["tests/test_colors.py", "-vv"])


if __name__ == '__main__':
    test_to_rgb()
    test_to_hex()
    test_add_comments()
    # run_tests()
    print("Done!")
