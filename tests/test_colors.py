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

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_RGB)
    print(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    print(s)
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

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_HEX)
    # print(json.dumps(d, indent=4))
    pp = PrettyPrinter(indent=0, newlinechar=" ", quote="'")
    s = pp.pprint(d)
    print(s)
    exp = "STYLE COLOR '#ff0000' OUTLINECOLOR '#00ff00' COLORRANGE '#000000' '#ffffff' END"
    assert s == exp


def test_add_rgb_comment():
    s = """
    STYLE
        COLOR 255 0 0
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_HEX, include_color_names=True)
    jsn = json.dumps(d, indent=4)
    print(jsn)
    assert d["__comments__"]["color"][0] == "# red"
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    print(s)
    exp = """STYLE
COLOR '#ff0000' # red
END"""

    assert s == exp


def test_add_hex_comment():
    s = """
    STYLE
        COLOR "#ff0000"
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_RGB, include_color_names=True)
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    exp = """STYLE
COLOR 255 0 0 # red
END"""

    assert s == exp


def test_add_comment_no_conversion():
    s = """
    STYLE
        COLOR "#ff0000"
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.NO_CONVERSION, include_color_names=True)
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    exp = """STYLE
COLOR '#ff0000' # red
END"""

    print(s)
    assert s == exp


def test_add_comment_no_conversion_rgb():
    s = """
    STYLE
        COLOR 255 0 0
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.NO_CONVERSION, include_color_names=True)
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    exp = """STYLE
COLOR 255 0 0 # red
END"""

    print(s)
    assert s == exp


def test_add_rgb_colorrange_comment():
    s = """
    STYLE
        COLORRANGE 0 0 0 255 255 255
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_HEX, include_color_names=True)
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    print(s)
    exp = """STYLE
COLORRANGE '#000000' '#ffffff' # black # white
END"""

    assert s == exp


@pytest.mark.xfail
def test_add_hex_colorrange_comment():
    """
    TODO Need to implement this
    """
    s = """
    STYLE
        COLORRANGE '#000000' '#ffffff'
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_RGB, include_color_names=True)
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    print(s)
    exp = """STYLE
COLORRANGE 0 0 0 255 255 255 # black # white
END"""

    assert s == exp


def test_add_to_existing_comments():
    s = """
    STYLE
        COLOR 255 0 0 # my color
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_HEX, include_color_names=True, include_comments=True)
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    print(s)
    exp = """STYLE
COLOR '#ff0000' # my color # red
END"""

    assert s == exp


def test_add_only_color_comment():
    """
    This requires using mappyfile classes
    """
    s = """
    STYLE
        COLOR 255 0 0 # my color
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_HEX, include_color_names=True, include_comments=False)
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    print(s)
    exp = """STYLE
COLOR '#ff0000' # red
END"""

    assert s == exp


def test_avoid_adding_colorname_twice():
    """
    This requires using mappyfile classes
    """
    s = """
    STYLE
        COLOR '#ff0000' # red
    END
    """

    d = mappyfile_colors.colors_transform(s, ConversionType.TO_HEX, include_color_names=True, include_comments=True)
    pp = PrettyPrinter(indent=0, quote="'")
    s = pp.pprint(d)
    print(s)

    exp = """STYLE
COLOR '#ff0000' # red
END"""

    assert s == exp


def run_tests():
    pytest.main(["tests/test_colors.py", "-vv"])


if __name__ == '__main__':
    # test_avoid_adding_colorname_twice()
    test_add_comment_no_conversion_rgb()
    run_tests()
    print("Done!")
