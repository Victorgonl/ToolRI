import enum
import typing

# TODO: update to enum and delete this
FG_COLOR = "#222222"
TEXT_COLOR = "#FFFFFF"
HOVER_COLOR = "#303030"
BG_COLOR = FG_COLOR
TEXT_FG_COLOR = "#343434"

BLACK = "#000000"
WHITE = "#FFFFFF"


class ColorPalette(enum.Enum):

    # Brasil colours
    # - https://www.gov.br/secom/pt-br/central-de-conteudo/manuais/uso-da-marca-do-governo-federal/2023-jan_br_govfederal_manual-de-uso_v1.1/@@download/file
    vermelho_urucum = "#FF0000"  # Vermelho-Urucum
    amarelo_sol = "#FFD000"  # Amarelo-Sol
    azul_atlantico = "#183EFF"  # Azul-Atlântico
    verde_amazonia = "#00D000"  # Verde-Amazônia
    preto_ebano = "#000000"  # Preto-Ébano
    branco_paz = "#FFFFFF"  # Branco-Paz
    cinza_harpia = "#3C3C3C"  # Cinza-Hárpia

    # UFLA colours
    # - https://ufla.br/images/arquivos/comunicacao/Manual_de_Identidade_Visual_da_UFLA.pdf
    azul_ufla = "#004B80"  # Azul-UFLA
    verde_ufla = "#00943E"  # Verde-UFLA
    cinza_ufla_claro = "#97B1BF"  # Cinza-UFLA Claro
    azul_ufla_claro = "#0087C0"  # Azul-UFLA Claro
    verde_ufla_claro = "#A8CF45"  #  Verde-UFLA Claro
    cinza_ufla_escuro = "#5C6C75"  # Cinza-UFLA Escuro
    azul_ufla_escuro = "#064B76"  # Azul-UFLA Escuro
    verde_ufla_escuro = "#006B3E"  # Verde-UFLA Escuro

    # ToolRI
    scarlet = "#DE1F26"
    cherry_red = "#ED1D24"
    yellowish_orange = "#F6A800"
    golden_yellow = "#FFCB05"

    # Tableau Palette
    tableau_blue = "#1f77b4"
    tableau_orange = "#ff7f0e"
    tableau_green = "#2ca02c"
    tableau_red = "#d62728"
    tableau_purple = "#9467bd"
    tableau_brown = "#8c564b"
    tableau_pink = "#e377c2"
    tableau_gray = "#7f7f7f"
    tableau_olive = "#bcbd22"
    tableau_cyan = "#17becf"

    # CSS colours
    aliceblue = "#F0F8FF"
    antiquewhite = "#FAEBD7"
    aqua = "#00FFFF"
    aquamarine = "#7FFFD4"
    azure = "#F0FFFF"
    beige = "#F5F5DC"
    bisque = "#FFE4C4"
    black = "#000000"
    blanchedalmond = "#FFEBCD"
    blue = "#0000FF"
    blueviolet = "#8A2BE2"
    brown = "#A52A2A"
    burlywood = "#DEB887"
    cadetblue = "#5F9EA0"
    chartreuse = "#7FFF00"
    chocolate = "#D2691E"
    coral = "#FF7F50"
    cornflowerblue = "#6495ED"
    cornsilk = "#FFF8DC"
    crimson = "#DC143C"
    cyan = "#00FFFF"
    darkblue = "#00008B"
    darkcyan = "#008B8B"
    darkgoldenrod = "#B8860B"
    darkgray = "#A9A9A9"
    darkgreen = "#006400"
    darkgrey = "#A9A9A9"
    darkkhaki = "#BDB76B"
    darkmagenta = "#8B008B"
    darkolivegreen = "#556B2F"
    darkorange = "#FF8C00"
    darkorchid = "#9932CC"
    darkred = "#8B0000"
    darksalmon = "#E9967A"
    darkseagreen = "#8FBC8F"
    darkslateblue = "#483D8B"
    darkslategray = "#2F4F4F"
    darkslategrey = "#2F4F4F"
    darkturquoise = "#00CED1"
    darkviolet = "#9400D3"
    deeppink = "#FF1493"
    deepskyblue = "#00BFFF"
    dimgray = "#696969"
    dimgrey = "#696969"
    dodgerblue = "#1E90FF"
    firebrick = "#B22222"
    floralwhite = "#FFFAF0"
    forestgreen = "#228B22"
    fuchsia = "#FF00FF"
    gainsboro = "#DCDCDC"
    ghostwhite = "#F8F8FF"
    gold = "#FFD700"
    goldenrod = "#DAA520"
    gray = "#808080"
    green = "#008000"
    greenyellow = "#ADFF2F"
    grey = "#808080"
    honeydew = "#F0FFF0"
    hotpink = "#FF69B4"
    indianred = "#CD5C5C"
    indigo = "#4B0082"
    ivory = "#FFFFF0"
    khaki = "#F0E68C"
    lavender = "#E6E6FA"
    lavenderblush = "#FFF0F5"
    lawngreen = "#7CFC00"
    lemonchiffon = "#FFFACD"
    lightblue = "#ADD8E6"
    lightcoral = "#F08080"
    lightcyan = "#E0FFFF"
    lightgoldenrodyellow = "#FAFAD2"
    lightgray = "#D3D3D3"
    lightgreen = "#90EE90"
    lightgrey = "#D3D3D3"
    lightpink = "#FFB6C1"
    lightsalmon = "#FFA07A"
    lightseagreen = "#20B2AA"
    lightskyblue = "#87CEFA"
    lightslategray = "#778899"
    lightslategrey = "#778899"
    lightsteelblue = "#B0C4DE"
    lightyellow = "#FFFFE0"
    lime = "#00FF00"
    limegreen = "#32CD32"
    linen = "#FAF0E6"
    magenta = "#FF00FF"
    maroon = "#800000"
    mediumaquamarine = "#66CDAA"
    mediumblue = "#0000CD"
    mediumorchid = "#BA55D3"
    mediumpurple = "#9370DB"
    mediumseagreen = "#3CB371"
    mediumslateblue = "#7B68EE"
    mediumspringgreen = "#00FA9A"
    mediumturquoise = "#48D1CC"
    mediumvioletred = "#C71585"
    midnightblue = "#191970"
    mintcream = "#F5FFFA"
    mistyrose = "#FFE4E1"
    moccasin = "#FFE4B5"
    navajowhite = "#FFDEAD"
    navy = "#000080"
    oldlace = "#FDF5E6"
    olive = "#808000"
    olivedrab = "#6B8E23"
    orange = "#FFA500"
    orangered = "#FF4500"
    orchid = "#DA70D6"
    palegoldenrod = "#EEE8AA"
    palegreen = "#98FB98"
    paleturquoise = "#AFEEEE"
    palevioletred = "#DB7093"
    papayawhip = "#FFEFD5"
    peachpuff = "#FFDAB9"
    peru = "#CD853F"
    pink = "#FFC0CB"
    plum = "#DDA0DD"
    powderblue = "#B0E0E6"
    purple = "#800080"
    rebeccapurple = "#663399"
    red = "#FF0000"
    rosybrown = "#BC8F8F"
    royalblue = "#4169E1"
    saddlebrown = "#8B4513"
    salmon = "#FA8072"
    sandybrown = "#F4A460"
    seagreen = "#2E8B57"
    seashell = "#FFF5EE"
    sienna = "#A0522D"
    silver = "#C0C0C0"
    skyblue = "#87CEEB"
    slateblue = "#6A5ACD"
    slategray = "#708090"
    slategrey = "#708090"
    snow = "#FFFAFA"
    springgreen = "#00FF7F"
    steelblue = "#4682B4"
    tan = "#D2B48C"
    teal = "#008080"
    thistle = "#D8BFD8"
    tomato = "#FF6347"
    turquoise = "#40E0D0"
    violet = "#EE82EE"
    wheat = "#F5DEB3"
    white = "#FFFFFF"
    whitesmoke = "#F5F5F5"
    yellow = "#FFFF00"
    yellowgreen = "#9ACD32"


# TODO: use only enum and delete this
def ToolRIColorPallete(color_format: typing.Literal["hex", "rgb"] = "hex") -> dict:

    color_pallete_hex = {
        color_name: color_value.value
        for color_name, color_value in ColorPalette.__members__.items()
    }

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)
        return red, green, blue

    color_pallete_rgb = {}
    if color_format == "hex":
        return color_pallete_hex
    else:
        for color_name, hex_value in color_pallete_hex.items():
            rgb_value = hex_to_rgb(hex_value)
            color_pallete_rgb[color_name] = rgb_value
        return color_pallete_rgb
