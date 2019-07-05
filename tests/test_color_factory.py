import mappyfile_colors
import pytest


def test_get_colors():

    color_factory = mappyfile_colors.ColorFactory()
    palette_name = "maximum_contrast"
    clrs = color_factory.get_colors(palette_name)

    for c in clrs:
        print(c, mappyfile_colors.hex_to_name(c))

    raised = False

    try:
        next(clrs)
    except StopIteration:
        raised = True

    assert raised


def test_get_infinite_colors():

    color_factory = mappyfile_colors.ColorFactory()
    palette_name = "maximum_contrast"
    clrs = color_factory.get_colors(palette_name, repeat=True)
    # print(list(clrs))  # Don't ever do this with repeat=True!

    for i, c in enumerate(clrs):
        print(i, c)
        if i == 100:
            break

    assert i == 100


def test_get_palette_names():

    color_factory = mappyfile_colors.ColorFactory()
    palette_names = color_factory.palette_names
    assert len(palette_names) > 0


def run_tests():
    pytest.main(["tests/test_color_factory.py", "-vv"])


if __name__ == '__main__':
    test_get_colors()
    test_get_infinite_colors()
    test_get_palette_names()
    run_tests()
    print("Done!")
