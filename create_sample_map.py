"""
ID,WKT
1,"CIRCULARSTRING(0 0, 10 10, 20 0)"
2,"CIRCULARSTRING(0 0, 10 10, 20 0)"

C:\MapServer\SDKShell.bat
REM cd C:\Code\mappyfile-colors
cd /D D:\GitHub\mappyfile-colors
shp2img -m example.map -o rainbow.png -map_debug 5 -layer_debug curves 5

"""

import csv
import mappyfile
import copy


with open("curves.csv", "w") as f:
    writer = csv.writer(f, dialect='excel')
    writer.writerow(("ID", "WKT"))
    multiplier = 3
    for i in range(1, 8):
        row = (i, "CIRCULARSTRING(0 0, 75 100, 150 0)")
        start_x = 0 - i * multiplier
        end_x = 150 + i * multiplier
        offset_x = 75 + (i * multiplier)
        offset_y = 100 + (i * multiplier)
        row = (i, "CIRCULARSTRING({} 0, {} {}, {} 0)".format(start_x,
                                                             offset_x, offset_y, end_x))
        print(row)
        writer.writerow(row)
 
template = """
CLASS
    EXPRESSION ([ID] = 1)
    STYLE
        LINECAP BUTT
        WIDTH 12
        COLOR 255 0 0
        OFFSET 0 -99
    END
END
"""

# colours of the rainbow

colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', 
          '#0000FF', '#4B0082', '#9400D3']

colors = list(reversed(colors))
tmpl_cls = mappyfile.loads(template)
rainbow_classes = []

for i in range(1, 8):
    new_cls = copy.deepcopy(tmpl_cls)
    style = new_cls["styles"][0]
    new_cls["expression"] = "([ID] = {})".format(i)
    style["color"] = colors[i-1]
    # style["offset"][0] = i * style["width"] * -1
    rainbow_classes.append(new_cls)

mappyfile.save(rainbow_classes, "rainbow_classes.txt")
print("Done!")

