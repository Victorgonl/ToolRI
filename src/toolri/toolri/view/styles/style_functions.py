import colorsys


def darken_hex_color(hex_color, factor=0.15):
    hex_color = hex_color.lstrip("#")
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    l = max(0, min(1, l - factor))
    r, g, b = tuple(round(val * 255) for val in colorsys.hls_to_rgb(h, l, s))
    return "#{:02x}{:02x}{:02x}".format(r, g, b)
