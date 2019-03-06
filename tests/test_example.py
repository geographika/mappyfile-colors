"""
Test the example on the README page
"""


def test_example():

    import mappyfile
    # from mappyfile.plugins import mappyfile_colors
    from mappyfile_colors import ColorsTransformer, ConversionType

    s = """
    CLASS
        STYLE
            COLOR 184 134 11
            OUTLINECOLOR 0 0 255
            WIDTH 3
        END
    END
    """

    d = mappyfile.loads(s, include_color_names=True, transformerClass=ColorsTransformer,
                        conversion_type=ConversionType.TO_HEX)
    print(mappyfile.dumps(d))

    s = mappyfile.dumps(d)
    assert s == """CLASS
    STYLE
        COLOR "#b8860b"
        OUTLINECOLOR "#0000ff"
        WIDTH 3
    END
END"""


test_example()
