#!/usr/bin/env python3
"""Rysuje 3 rysunki pliku README.md i sprawdza liczby. Uzycie: figures.py [--check]"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

# Pastele i tony srednie: niebieski, pomaranczowy, zolty, zielony, szary.
B, BM = "#9CCDE8", "#2F7CC4"
O, OM = "#F6BD78", "#D97757"
Y = "#F7DD72"
G, GM = "#B7DFA4", "#2E8B57"
K, KM = "#D1D1D1", "#878787"
INK, MUTED, ACCENT, PAPER = "#33322e", "#6b6a63", "#1f5f9e", "#FBF8F1"


# ---------- czesci rysunku: plama koloru, kontur, cienka linia ----------

def patch(d, c, o=None):
    op = f" opacity='{o}'" if o else ""
    return f"<path d='{d}' fill='{c}'{op}/>"


def pen(d, w=2.5, dash=None):
    da = f" stroke-dasharray='{dash}'" if dash else ""
    return (f"<path d='{d}' fill='none' stroke='currentColor' stroke-width='{w}' "
            f"stroke-linecap='round' stroke-linejoin='round'{da}/>")


def fine(d):
    return pen(d, 1.2)


def blob(cx, cy, rx, ry, c, o=None):
    op = f" opacity='{o}'" if o else ""
    return f"<ellipse cx='{cx}' cy='{cy}' rx='{rx}' ry='{ry}' fill='{c}'{op}/>"


def ring(cx, cy, rx, ry, w=2.5):
    return (f"<ellipse cx='{cx}' cy='{cy}' rx='{rx}' ry='{ry}' fill='none' "
            f"stroke='currentColor' stroke-width='{w}'/>")


def box(x, y, w, h):
    return f"M{x} {y} L{x + w} {y} L{x + w} {y + h} L{x} {y + h} Z"


# ---------- obiekty gospodarstwa: kazdy obiekt ma pole 200 x 160 ----------

def table():
    return [
        blob(104, 143, 80, 8, KM, 0.3),
        patch("M26 78 L34 83 L34 128 L26 124 Z", O),
        patch("M171 82 L180 80 L180 126 L171 128 Z", O),
        patch("M22 68 L138 50 L182 72 L62 96 Z", O),
        patch("M22 68 L62 96 L182 72 L182 80 L62 104 L22 76 Z", O),
        patch("M22 68 L62 96 L182 72 L182 80 L62 104 L22 76 Z", OM, 0.3),
        patch("M57 103 L67 103 L67 148 L57 148 Z", O),
        patch("M62 103 L67 103 L67 148 L62 148 Z", OM, 0.3),
        pen("M22 68 L138 50 L182 72 L62 96 Z"),
        pen("M22 68 L22 76 L62 104 L182 80 L182 72 M62 96 L62 104"),
        pen("M26 79 L26 124 L34 128 L34 85"),
        pen("M57 104 L57 148 L67 148 L67 104"),
        pen("M171 83 L171 128 L180 126 L180 81"),
        blob(104, 73, 27, 9.5, Y),
        ring(104, 73, 27, 9.5),
        ring(104, 73, 18, 6, 1.2),
        blob(104, 71, 12, 4.5, G),
        fine("M97 60 Q93 53 98 47 Q102 41 98 35"),
        fine("M110 59 Q106 52 111 46 Q115 40 111 34"),
        patch("M56 71 L72 71 L70 83 Q64 86 58 83 Z", B),
        fine("M56 71 L58 83 Q64 86 70 83 L72 71"),
        ring(64, 71, 8, 2.8, 1.2),
        fine("M72 74 Q79 75 71 81"),
        fine("M136 79 L152 73"),
        ring(156, 72, 4.5, 2.6, 1.2),
    ]


def hatch():
    return [
        patch(box(28, 36, 88, 70), KM, 0.3),
        patch(box(20, 28, 104, 8), O),
        patch(box(20, 36, 8, 70), O),
        patch(box(116, 36, 8, 70), O),
        patch("M52 70 L92 70 L90 96 Q72 100 54 96 Z", B),
        fine("M52 70 L54 96 Q72 100 90 96 L92 70 Z"),
        fine("M46 76 L52 76 M92 76 L98 76"),
        fine("M64 62 Q60 56 65 50 M80 62 Q76 56 81 50"),
        patch("M12 106 L132 106 L142 118 L2 118 Z", O),
        patch(box(2, 118, 140, 8), O),
        patch(box(2, 118, 140, 8), OM, 0.3),
        pen("M20 106 L20 28 L124 28 L124 106"),
        pen("M28 106 L28 36 L116 36 L116 106"),
        pen("M12 106 L132 106 L142 118 L2 118 Z"),
        pen("M2 118 L2 126 L142 126 L142 118"),
        blob(74, 111, 24, 6, Y),
        ring(74, 111, 24, 6),
        blob(74, 109, 13, 4, G),
        patch(box(150, 40, 40, 64), Y),
        pen(box(150, 40, 40, 64)),
        fine("M160 40 L170 24 L180 40"),
        blob(170, 24, 2.5, 2.5, KM),
        fine("M157 54 L183 54 M157 64 L183 64 M157 74 L176 74 M157 84 L183 84 M157 94 L170 94"),
    ]


def stove():
    return [
        blob(100, 147, 76, 8, KM, 0.3),
        patch(box(36, 72, 90, 70), K),
        patch("M126 72 L160 56 L160 126 L126 142 Z", K),
        patch("M126 72 L160 56 L160 126 L126 142 Z", KM, 0.3),
        patch("M36 72 L126 72 L160 56 L70 56 Z", K),
        blob(98, 64, 25, 5, KM, 0.55),
        pen(box(36, 72, 90, 70)),
        pen("M126 72 L160 56 L160 126 L126 142"),
        pen("M36 72 L70 56 L160 56"),
        patch("M140 6 L152 6 L152 58 L140 63 Z", K),
        patch("M146 6 L152 6 L152 58 L146 60 Z", KM, 0.3),
        pen("M140 6 L140 63 M152 6 L152 58 M140 6 L152 6"),
        patch(box(56, 98, 50, 26), O),
        patch("M64 124 Q70 104 77 124 Z", Y),
        patch("M82 124 Q89 100 96 124 Z", Y),
        pen(box(48, 88, 66, 44), 1.2),
        pen(box(56, 98, 50, 26), 1.2),
        fine("M56 93 L106 93"),
        patch("M76 40 L120 40 L118 60 Q98 66 78 60 Z", B),
        patch("M100 40 L120 40 L118 60 Q108 64 100 64 Z", BM, 0.3),
        pen("M76 40 L78 60 Q98 66 118 60 L120 40"),
        ring(98, 40, 22, 6),
        fine("M70 47 L76 47 M120 47 L126 47"),
        blob(98, 37, 3.5, 2.5, KM),
        fine("M90 28 Q86 22 91 16 Q95 10 91 4"),
        fine("M106 28 Q102 22 107 16 Q111 10 107 4"),
    ]


def cellar():
    out = [
        patch("M4 142 Q22 44 100 30 Q178 44 196 142 Z", G),
        patch("M100 30 Q178 44 196 142 L160 142 L160 72 Q132 46 100 40 Z", GM, 0.3),
        patch("M40 142 L40 72 Q100 40 160 72 L160 142 Z", K),
        pen("M40 142 L40 72 Q100 40 160 72 L160 142"),
        fine("M144 92 L156 96 M142 116 L156 118 M146 134 L158 132 M84 60 L96 56 M108 55 L120 59"),
        patch("M62 142 L62 86 Q100 64 138 86 L138 142 Z", KM, 0.55),
        pen("M62 142 L62 86 Q100 64 138 86 L138 142"),
        fine("M64 100 L136 100 M64 122 L136 122"),
    ]
    for x, y, c in [(72, 84, O), (92, 82, Y), (112, 84, O), (74, 106, Y), (94, 106, O)]:
        h = (100 if y < 100 else 122) - y
        out.append(patch(box(x, y, 12, h), c))
        out.append(fine(box(x, y, 12, h) + " " + box(x + 2, y - 3, 8, 3)))
    out += [
        patch(box(110, 126, 24, 16), Y),
        pen(box(110, 126, 24, 16), 1.2),
        fine("M110 131 L134 131 M110 136 L134 136"),
        patch("M62 88 L42 94 L42 142 L62 142 Z", O),
        patch("M62 88 L42 94 L42 142 L62 142 Z", OM, 0.3),
        pen("M62 88 L42 94 L42 142 L62 142"),
        fine("M49 92 L49 142 M55 90 L55 142"),
        blob(58, 116, 2, 2, KM),
        pen("M4 142 L196 142"),
        fine("M22 118 L26 108 M30 120 L33 111 M168 112 L171 102 M176 118 L180 109 M96 26 L99 18 M104 26 L107 19"),
    ]
    return out


def well():
    return [
        blob(100, 145, 62, 8, KM, 0.3),
        patch("M60 96 L60 132 Q100 148 140 132 L140 96 Z", K),
        patch("M100 96 L140 96 L140 132 Q122 142 100 144 Z", KM, 0.3),
        blob(100, 96, 40, 12, K),
        blob(100, 97, 30, 8, B),
        patch("M64 44 L71 44 L71 92 L64 90 Z", O),
        patch("M129 44 L136 44 L136 90 L129 92 Z", O),
        pen("M64 46 L64 90 M71 46 L71 91 M129 46 L129 91 M136 46 L136 90"),
        ring(100, 96, 40, 12),
        ring(100, 97, 30, 8, 1.2),
        pen("M60 96 L60 132 Q100 148 140 132 L140 96"),
        fine("M60 116 Q100 132 140 116 M78 108 L78 123 M118 126 L118 141 M98 128 L98 143 M130 106 L130 120"),
        patch("M46 48 L100 16 L154 48 Z", O),
        patch("M100 16 L154 48 L100 48 Z", OM, 0.3),
        pen("M46 48 L100 16 L154 48 Z"),
        pen("M71 62 L129 62"),
        pen("M136 62 L148 62 L148 76"),
        fine("M100 62 L100 80"),
        patch("M92 82 L108 82 L106 96 L94 96 Z", B),
        pen("M92 82 L108 82 L106 96 L94 96 Z", 1.2),
        fine("M93 82 Q100 74 107 82"),
    ]


def tank():
    return [
        blob(100, 147, 72, 8, KM, 0.3),
        patch("M58 130 L74 134 L74 144 L58 140 Z", K),
        patch("M126 134 L142 130 L142 140 L126 144 Z", K),
        pen("M58 132 L58 140 L74 144 L74 136 M126 136 L126 144 L142 140 L142 132", 1.2),
        patch("M50 44 L50 122 Q100 138 150 122 L150 44 Z", B),
        patch("M112 44 L150 44 L150 122 Q132 132 112 134 Z", BM, 0.3),
        blob(100, 44, 50, 13, B),
        blob(100, 42, 14, 4, K),
        ring(100, 44, 50, 13),
        ring(100, 42, 14, 4, 1.2),
        pen("M50 44 L50 122 Q100 138 150 122 L150 44"),
        fine("M50 70 Q100 86 150 70 M50 96 Q100 112 150 96"),
        fine("M62 64 L62 120 M59 74 L65 74 M59 88 L65 88 M59 102 L65 102 M59 116 L65 116"),
        patch(box(150, 108, 30, 8), K),
        pen("M150 108 L180 108 M150 116 L180 116 M180 105 L180 119"),
        pen("M166 108 L166 98 M160 98 L172 98"),
        patch("M186 122 Q181 131 186 135 Q191 131 186 122 Z", B),
    ]


def pv():
    return [
        blob(104, 147, 82, 7, KM, 0.3),
        blob(30, 26, 12, 12, Y),
        fine("M30 8 L30 2 M30 44 L30 50 M12 26 L6 26 M17 13 L13 9 M43 13 L47 9 M17 39 L13 43"),
        pen("M176 44 L184 140 M148 126 L184 140 M148 126 L148 137 M22 112 L22 123"),
        patch("M22 112 L148 126 L176 44 L50 30 Z", B),
        patch("M22 112 L148 126 L162 85 L36 71 Z", BM, 0.3),
        pen("M22 112 L148 126 L176 44 L50 30 Z"),
        fine("M53.5 115.5 L81.5 33.5 M85 119 L113 37 M116.5 122.5 L144.5 40.5 M36 71 L162 85"),
    ]


def coop():
    return [
        patch("M6 138 Q100 126 194 140 L194 150 Q100 156 6 150 Z", G),
        patch("M112 62 L172 52 L172 114 L112 126 Z", O),
        patch("M112 62 L172 52 L172 114 L112 126 Z", OM, 0.3),
        patch("M52 62 L82 30 L112 62 L112 126 L52 126 Z", O),
        patch("M82 30 L142 22 L172 52 L112 62 Z", K),
        patch("M82 30 L142 22 L172 52 L112 62 Z", KM, 0.3),
        pen("M52 126 L52 62 L82 30 L112 62 L112 126 Z"),
        pen("M112 62 L172 52 L172 114 L112 126"),
        pen("M82 30 L142 22 L172 52"),
        patch(box(72, 98, 20, 28), KM, 0.55),
        patch(box(72, 70, 20, 26), Y),
        pen(box(72, 70, 20, 26), 1.2),
        fine("M69 66 L69 126 M95 66 L95 126"),
        patch(box(76, 54, 12, 9), B),
        pen(box(76, 54, 12, 9) + " M82 63 L82 70", 1.2),
        patch("M70 126 L94 126 L88 148 L58 148 Z", Y),
        pen("M70 126 L94 126 L88 148 L58 148 Z", 1.2),
        fine("M67 132 L92 132 M64 138 L91 138 M61 144 L89 144"),
        fine("M130 78 L154 74 L154 94 L130 98 Z M142 76 L142 96"),
        blob(30, 130, 13, 9, Y),
        blob(18, 118, 5.5, 5.5, Y),
        patch("M41 124 L52 115 L47 132 Z", Y),
        patch("M15 113 L18 107 L21 113 Z", OM),
        patch("M13 117 L7 120 L13 122 Z", O),
        pen("M24 120 Q33 118 41 124 L52 115 L47 132 Q42 140 30 139 Q18 139 17 128 L17 123", 1.2),
        ring(18, 118, 5.5, 5.5, 1.2),
        fine("M26 138 L26 146 M33 139 L33 146"),
        blob(16.5, 117, 1, 1, KM),
        blob(170, 134, 12, 8, Y),
        blob(181, 123, 5, 5, Y),
        patch("M160 129 L150 121 L154 136 Z", Y),
        patch("M178 118 L181 113 L184 118 Z", OM),
        patch("M186 122 L192 125 L186 127 Z", O),
        pen("M176 125 Q167 124 160 129 L150 121 L154 136 Q160 142 170 142 Q182 142 182 133 L182 128", 1.2),
        ring(181, 123, 5, 5, 1.2),
        fine("M167 141 L167 148 M174 142 L174 148"),
        blob(182.5, 122, 1, 1, KM),
    ]


def excavator():
    return [
        blob(96, 149, 86, 7, KM, 0.3),
        patch("M150 146 Q166 122 188 146 Z", O),
        pen("M150 146 Q166 122 188 146", 1.2),
        patch("M36 126 Q26 126 26 135 Q26 146 38 146 L120 146 Q132 146 132 135 Q132 126 122 126 Z", KM),
        pen("M36 126 Q26 126 26 135 Q26 146 38 146 L120 146 Q132 146 132 135 Q132 126 122 126 Z"),
        ring(40, 136, 6, 6, 1.2),
        ring(118, 136, 6, 6, 1.2),
        ring(66, 137, 4, 4, 1.2),
        ring(92, 137, 4, 4, 1.2),
        patch(box(42, 100, 84, 26), Y),
        patch(box(96, 100, 30, 26), OM, 0.3),
        patch("M50 64 L90 64 L98 100 L50 100 Z", Y),
        patch("M57 70 L85 70 L90 94 L57 94 Z", B),
        pen(box(42, 100, 84, 26)),
        pen("M50 100 L50 64 L90 64 L98 100"),
        pen("M57 70 L85 70 L90 94 L57 94 Z", 1.2),
        fine("M104 108 L120 108 M104 114 L120 114 M104 120 L120 120"),
        patch("M94 92 L132 34 L142 40 L106 96 Z", Y),
        pen("M94 92 L132 34 L142 40 L106 96 Z"),
        patch("M132 34 L142 30 L176 82 L166 88 Z", Y),
        patch("M132 34 L142 30 L176 82 L166 88 Z", OM, 0.3),
        pen("M132 34 L142 30 L176 82 L166 88 Z"),
        fine("M104 80 L128 50 M150 36 L164 60"),
        blob(137, 36, 3, 3, KM),
        patch("M160 86 L180 84 L178 108 Q166 114 156 102 Z", K),
        pen("M160 86 L180 84 L178 108 Q166 114 156 102 Z"),
        fine("M160 106 L158 112 M166 110 L165 116 M172 110 L173 116"),
    ]


def fence():
    mesh = [(18, 62, 66, 110), (18, 88, 66, 136), (42, 62, 66, 86), (66, 62, 18, 110), (66, 88, 18, 136), (42, 62, 18, 86)]
    left = " ".join(f"M{a} {b} L{c} {d}" for a, b, c, d in mesh)
    right = " ".join(f"M{a + 116} {b} L{c + 116} {d}" for a, b, c, d in mesh)
    out = [patch(box(4, 138, 192, 10), G)]
    out += [fine(left), fine(right)]
    out.append(pen("M18 60 L66 60 M134 60 L182 60 M18 137 L66 137 M134 137 L182 137", 1.2))
    for x in (10, 66, 126, 182):
        out.append(patch(box(x, 46, 8, 98), O))
        out.append(pen(box(x, 46, 8, 98), 1.2))
        out.append(blob(x + 4, 41, 3, 3, KM))
    out += [
        patch(box(78, 62, 44, 74), O),
        patch(box(100, 62, 22, 74), OM, 0.3),
        pen(box(78, 62, 44, 74)),
        pen("M78 136 L122 62", 1.2),
        fine("M89 62 L89 136 M100 62 L100 136 M111 62 L111 136"),
        pen("M10 38 L190 38", 1.2, "6 5"),
        patch(box(146, 8, 26, 22), Y),
        pen(box(146, 8, 26, 22), 1.2),
        patch("M161 10 L154 20 L159 20 L156 28 L165 17 L160 17 Z", OM),
        fine("M159 30 L159 38"),
        patch(box(109, 96, 10, 10), Y),
        fine(box(109, 96, 10, 10) + " M111 96 Q111 89 114 89 Q117 89 117 96"),
    ]
    return out


def generator():
    return [
        blob(100, 146, 68, 7, KM, 0.3),
        blob(64, 133, 9, 9, KM),
        ring(64, 133, 9, 9),
        blob(136, 133, 9, 9, KM),
        ring(136, 133, 9, 9),
        patch(box(46, 72, 108, 52), Y),
        patch(box(46, 112, 108, 12), OM, 0.3),
        patch(box(58, 80, 44, 36), K),
        fine("M62 86 L98 86 M62 92 L98 92 M62 98 L98 98 M62 104 L98 104 M62 110 L98 110"),
        blob(128, 98, 17, 19, K),
        blob(133, 98, 12, 19, KM, 0.3),
        ring(128, 98, 17, 19),
        ring(128, 98, 7, 8, 1.2),
        patch("M56 52 L144 52 L150 72 L50 72 Z", O),
        pen("M56 52 L144 52 L150 72 L50 72 Z"),
        blob(104, 50, 8, 3, KM),
        pen("M70 52 L70 38 L86 38"),
        fine("M92 36 Q98 30 94 24 M100 38 Q108 32 103 24"),
        pen(box(46, 72, 108, 52)),
        pen(box(58, 80, 44, 36), 1.2),
        pen("M154 84 L176 74 L176 80"),
    ]


def battery():
    out = [
        blob(100, 146, 62, 7, KM, 0.3),
        patch(box(52, 36, 72, 102), G),
        patch("M124 36 L150 26 L150 126 L124 138 Z", G),
        patch("M124 36 L150 26 L150 126 L124 138 Z", GM, 0.3),
        patch("M52 36 L124 36 L150 26 L78 26 Z", G),
        pen(box(52, 36, 72, 102)),
        pen("M124 36 L150 26 L150 126 L124 138"),
        pen("M52 36 L78 26 L150 26"),
        fine("M92 40 L92 134"),
    ]
    for i, y in enumerate((112, 98, 84, 70)):
        if i < 3:
            out.append(patch(box(60, y, 24, 10), Y))
        out.append(fine(box(60, y, 24, 10)))
    out += [
        pen("M100 60 L114 60 M107 53 L107 67", 1.2),
        pen("M100 86 L114 86", 1.2),
        pen("M150 100 Q170 104 172 128 L172 142"),
    ]
    return out


def floatvalve():
    return [
        patch(box(42, 80, 116, 50), B),
        patch(box(42, 106, 116, 24), BM, 0.3),
        fine("M42 80 Q60 76 78 80 Q96 84 114 80 Q136 76 158 80"),
        pen("M40 50 L40 132 L160 132 L160 50"),
        fine("M34 50 L166 50"),
        patch(box(6, 32, 42, 10), K),
        pen("M6 32 L48 32 M6 42 L48 42"),
        patch(box(48, 26, 16, 28), O),
        pen(box(48, 26, 16, 28)),
        pen("M64 44 L118 70"),
        blob(128, 76, 14, 14, O),
        patch("M114 76 Q128 94 142 76 Q142 90 128 90 Q114 90 114 76 Z", OM, 0.3),
        ring(128, 76, 14, 14),
        fine("M56 54 L56 66 M52 62 L56 68 L60 62"),
        patch(box(160, 116, 34, 8), K),
        pen("M160 116 L194 116 M160 124 L194 124"),
        fine("M172 124 L172 133 M184 124 L184 133"),
        patch("M172 138 Q169 144 172 147 Q175 144 172 138 Z", B),
    ]


PICS = {f.__name__: f for f in (table, hatch, stove, cellar, well, tank, pv, coop, excavator,
                                fence, generator, battery, floatvalve)}


# ---------- skladanie rysunkow ----------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=15, weight=400, fill=INK, anchor="middle", mono=False):
    fam = " font-family='DejaVu Sans Mono, Consolas, Menlo, monospace'" if mono else ""
    return (f"<text x='{x:g}' y='{y:g}' font-size='{size}' font-weight='{weight}' fill='{fill}' "
            f"text-anchor='{anchor}'{fam}>{esc(s)}</text>")


def arrow(x1, y, x2, dash=False):
    da = " stroke-dasharray='5 5'" if dash else ""
    return (f"<line x1='{x1}' y1='{y}' x2='{x2 - 8}' y2='{y}' stroke='{MUTED}' stroke-width='2.5' "
            f"stroke-linecap='round'{da}/>"
            f"<path d='M{x2 - 9} {y - 6} L{x2} {y} L{x2 - 9} {y + 6}' fill='none' stroke='{MUTED}' "
            f"stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'/>")


def embed(name, x, y, w):
    return (f"<svg x='{x:g}' y='{y:g}' width='{w:g}' height='{w * 0.8:g}' viewBox='0 0 200 160'>"
            + "".join(PICS[name]()) + "</svg>")


def caption(cx, y, name, part, note):
    return (text(cx, y, name, 15, 700) + text(cx, y + 21, part, 14, 400, ACCENT)
            + text(cx, y + 40, note, 12.5, 400, MUTED))


def frame(w, h, title, body):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' "
            f"color='{INK}' font-family='DejaVu Sans, Verdana, Arial, sans-serif'>"
            f"<rect width='{w}' height='{h}' rx='18' fill='{PAPER}'/>"
            + text(w / 2, 44, title, 22, 700) + "".join(body).replace("currentColor", INK) + "</svg>\n")


def row(items, x0, y0, w, gap, arrows):
    body = []
    for i, (pic, name, part, note) in enumerate(items):
        x = x0 + i * (w + gap)
        body.append(embed(pic, x, y0, w))
        body.append(caption(x + w / 2, y0 + w * 0.8 + 30, name, part, note))
        if i and arrows[i - 1]:
            body.append(arrow(x - gap + 6, y0 + w * 0.45, x - 6, arrows[i - 1] == "dash"))
    return body


def fig1():
    items = [
        ("fence", "Ogrodzenie", "Bezpieczeństwo", "TLS, OAuth 2.0"),
        ("table", "Stół w jadalni", "Frontend", "React, TypeScript"),
        ("hatch", "Okienko z kartą dań", "Interfejs API", "REST"),
        ("stove", "Kuchnia drzewna", "Backend", "Spring, Node.js"),
        ("cellar", "Piwnica M1 i spichlerz", "Baza danych", "PostgreSQL"),
    ]
    body = row(items, 30, 78, 170, 35, [1, 1, 1, 1])
    body.append(f"<rect x='30' y='320' width='980' height='46' rx='12' fill='{G}' opacity='0.55'/>")
    body.append(text(520, 349, "Ziemia, budynki i przewody = infrastruktura: serwer, sieć, kontener, orkiestrator", 15))
    return frame(1040, 390, "Droga 1 żądania: od ogrodzenia do piwnicy M1", body)


def fig2():
    water = [
        ("well", "Studnia", "Pojedynczy punkt awarii", "1 studnia, 8 m głębokości"),
        ("tank", "Zbiornik górny W1", "Kolejka", "od 3 m³ do 5 m³"),
        ("floatvalve", "Zawór pływakowy W2", "Orkiestrator", "stan zadany: 60 dm³"),
        ("coop", "Budynek B1", "Mikroserwis: sterownik klapy", "klapa działa bez serwera"),
    ]
    power = [
        ("pv", "Stelaż fotowoltaiki", "Skalowanie", "56 modułów po 450 W"),
        ("battery", "Magazyn energii", "Element ze stanem", "30 kWh"),
        ("generator", "Agregat", "Replika", "start przy stanie 15 %"),
        ("excavator", "Koparka z operatorem", "Funkcja na żądanie", "od 4 h do 12 h pracy"),
    ]
    body = [text(40, 86, "Woda", 16, 700, MUTED, "start")]
    body += row(water, 40, 96, 190, 60, [1, 1, 1])
    body.append(text(40, 360, "Energia i praca", 16, 700, MUTED, "start"))
    body += row(power, 40, 370, 190, 60, [1, "dash", 0])
    return frame(1040, 620, "Infrastruktura i architektura w obiektach gospodarstwa", body)


def panel(x, y, head, pics, formula, lines):
    w, h = 340, 286
    out = [f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='14' fill='#FFFFFF' opacity='0.75'/>",
           text(x + 18, y + 30, head, 16, 700, INK, "start")]
    pw = 150 if len(pics) == 1 else 132
    px = x + (w - pw * len(pics) - 16 * (len(pics) - 1)) / 2
    for i, p in enumerate(pics):
        out.append(embed(p, px + i * (pw + 16), y + 42, pw))
    out.append(f"<rect x='{x + 14}' y='{y + 176}' width='{w - 28}' height='34' rx='8' fill='{B}' opacity='0.45'/>")
    out.append(text(x + w / 2, y + 198, formula, 13.5, 700, INK, "middle", True))
    for i, s in enumerate(lines):
        out.append(text(x + w / 2, y + 234 + i * 20, s, 12.5, 400, MUTED))
    return out


def fig3():
    n = numbers()
    panels = [
        ("1. Łańcuch zależności", ["well"], "Woda ⇔ Studnia ∧ Pompa ∧ Energia",
         ["Awaria 1 elementu zatrzymuje pobór wody.", f"0,99 · 0,99 · 0,99 = {n['chain']}"]),
        ("2. Redundancja", ["pv", "generator"], "Energia ⇔ (PV ∧ Magazyn) ∨ Agregat",
         [f"Bez agregatu: 1 − 6,1 / 365 = {n['pv']}", f"Z agregatem: 6,1 · 0,05 = {n['empty']} dnia na rok"]),
        ("3. Polecenie idempotentne", ["floatvalve"], "∀x: f(f(x)) = f(x)",
         ["„Napełnij do 60 dm³” spełnia wzór.", "„Dolej 10 dm³” nie spełnia wzoru."]),
        ("4. Twierdzenie CAP", ["coop"], "P ⇒ ¬(C ∧ A)",
         ["Przerwa łącza: klapa działa bez serwera.", "Serwer nie zna wtedy stanu klapy."]),
        ("5. Transakcja", ["cellar"], "Wydany ⇔ Przyjęty",
         ["Baza danych zapisuje oba wpisy", "albo żaden wpis."]),
        ("6. Skalowanie", ["pv"], "∀m1,m2 ∀z: Wynik(m1,z) = Wynik(m2,z)",
         ["20 kWp → 30 kWp: dni puste 13,6 → 3,0", "Magazyn energii ma stan: 30 kWh."]),
    ]
    body = []
    for i, (head, pics, formula, lines) in enumerate(panels):
        body += panel(20 + (i % 3) * 360, 70 + (i // 3) * 302, head, pics, formula, lines)
    return frame(1100, 690, "6 problemów we wzorach logiki matematycznej", body)


# ---------- liczby ----------

def pl(x, digits):
    return f"{x:.{digits}f}".replace(".", ",")


def numbers():
    pv_only = 1 - 6.1 / 365
    return {
        "chain": pl(0.99 ** 3, 6),
        "pv": pl(pv_only, 4),
        "both": pl(1 - (1 - pv_only) * (1 - 0.95), 4),
        "empty": pl(6.1 * 0.05, 1),
        "watts": f"{56 * 450:,}".replace(",", " "),
    }


def source_counts():
    proj = (ROOT / "projekt" / "PROJEKT.md").read_text(encoding="utf-8")
    sec16 = proj.split("## 16. Automatyzacja")[1].split("### Architektura sterowania")[0]
    rows = [l for l in sec16.splitlines() if l.startswith("| ") and not l.startswith(("| Układ", "| ---"))]
    ops = (ROOT / "operations" / "poultry-water-line.md").read_text(encoding="utf-8")
    sec6 = ops.split("## 6. Operacje wdrożenia")[1].split("## 7.")[0]
    oprows = [l for l in sec6.splitlines() if re.match(r"\| OP\d", l)]
    return {
        "systems": len(rows),
        "alarms": sum("Alarm:" in r for r in rows),
        "ops": len(oprows),
        "gates": sum("(bramka)" in r for r in oprows),
        "no_return": sum("(punkt bez powrotu)" in r for r in oprows),
    }


def check():
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    n, c = numbers(), source_counts()
    wanted = [
        n["chain"], n["pv"], n["both"], f"{n['empty']} dnia", f"{n['watts']} W",
        f"{c['alarms']} alarmów w {c['systems']} układach",
        f"{c['ops']} operacji", f"{c['gates']} bramki", f"{c['no_return']} punkt bez powrotu",
    ]
    missing = [w for w in wanted if w not in readme]
    for w in missing:
        print("brak w README.md:", w)
    print("sprawdzone liczby:", len(wanted), "braki:", len(missing))
    return 1 if missing else 0


def main():
    if "--check" in sys.argv:
        sys.exit(check())
    for name, fn in (("fig1-request-path.svg", fig1), ("fig2-infrastructure.svg", fig2), ("fig3-logic.svg", fig3)):
        (HERE / name).write_text(fn(), encoding="utf-8")
        print("zapisano", name)


if __name__ == "__main__":
    main()
