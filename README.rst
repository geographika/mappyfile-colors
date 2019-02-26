mappyfile-colors
================

| |Version| |Build Status|

A `mappyfile <http://mappyfile.readthedocs.io>`_ plugin to standardise and convert colors used in a Mapfile. 
Features include:

+ conversion between RGB and HEX colors
+ harmonise all colors in a Mapfile to either RGB or hex values
+ add `human readable color <https://en.wikipedia.org/wiki/X11_color_names#Color_name_chart>`_ names as comments
+ add color names to RGB color ranges as comments (*not currently possible for HEX color ranges*)
+ Python2 and 3 compatible

.. image:: https://raw.githubusercontent.com/geographika/mappyfile-colors/master/rainbow.png

Installation
------------

.. code-block:: console

    pip install mappyfile-colors

Note installing the ``mappyfile-colors`` plugin will automatically install the following 
dependencies:

* mappyfile
* webcolors

Online Demo
-----------

+ Go to the online mappyfile demo at http://mappyfile.geographika.net/
+ Select the "Rainbow colors" map
+ Open "Settings", the *mappyfile-colors Plugin Settings* section allows conversion to RGB and HEX, and to include
  color names as comments in the Mapfile output
+ Click the Format button

Usage
-----

To use the colors plugin, import it to a script, and then pass in a custom ``ColorsTransformer``. 
Two additional parameters can also be passed to the ``mappyfile.loads`` function:

+ ``include_color_names`` - set to True to add color names as comments (default is False)
+ ``conversion_type`` - a parameter to convert colors within a Mapfile, either import ``ConversionType`` or use an integer value
  to set the conversion:

  .. code-block:: python

      NO_CONVERSION = 0
      TO_RGB = 1
      TO_HEX = 2

A sample script to convert RGB to HEX colors, and include the color names is shown below. 

.. code-block:: python

    from mappyfile.plugins import mappyfile_colors 
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

    d = mappyfile.loads(s, include_color_names=True, include_comments=True, transformerClass=ColorsTransformer, conversion_type=ConversionType.TO_HEX)
    print(mappyfile.dumps(d))

This will output the following:

.. code-block:: bat

    CLASS 
        STYLE
            COLOR "#b8860b" # darkgoldenrod
            OUTLINECOLOR "#0000ff" # blue 
            WIDTH 3
        END
    END


See the `test_plugin.py`_ for further examples. 

Author
------

* Seth Girvin `@geographika <https://github.com/geographika>`_

.. |Version| image:: https://img.shields.io/pypi/v/mappyfile-colors.svg
   :target: https://pypi.python.org/pypi/mappyfile-colors

.. |Build Status| image:: https://travis-ci.org/geographika/mappyfile-colors.svg?branch=master
   :target: https://travis-ci.org/geographika/mappyfile-colors


.. _test_plugin.py: tests/test_plugin.py