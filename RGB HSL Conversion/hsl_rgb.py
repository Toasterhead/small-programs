#Adapted from formulas provided by RapidTables:

#https://www.rapidtables.com/convert/color/hsl-to-rgb.html
#https://www.rapidtables.com/convert/color/rgb-to-hsl.html

R = 0
G = 1
B = 2

H = 0
S = 1
L = 2

ALPHA = 3

FULL_ROTATION   = 360
MAX_COLOR_VALUE = 256

def hsl_to_rgb(color, hueInDegrees = True):

    """Converts from HSL to RGB color format."""

    assert type(color) in (tuple, list) and len(color) in (3, 4)
    assert type(hueInDegrees) == bool

    for i in color: assert type(i) in (int, float) and i >= 0

    assert color[S] <= 1 and color[L] <= 1

    if hueInDegrees == True:
        assert color[H] <= FULL_ROTATION
    else: assert color[H] <= 1

    color = list(color)

    if hueInDegrees == True:
        color[H] =  color[H] % FULL_ROTATION
    else:
        color[H] %= 1
        color[H]  = color[H] * FULL_ROTATION

    h = color[H]
    s = color[S]
    l = color[L]

    c = (1 - abs((2 * l) - 1)) * s
    x = c * (1 - abs(((h / 60) % 2) - 1))
    m = l - (c / 2)

    colorPrime = ()

    if      h >= 0      and h < 60:     colorPrime = (c, x, 0)
    elif    h >= 60     and h < 120:    colorPrime = (x, c, 0)
    elif    h >= 120    and h < 180:    colorPrime = (0, c, x)
    elif    h >= 180    and h < 240:    colorPrime = (0, x, c)
    elif    h >= 240    and h < 300:    colorPrime = (x, 0, c)
    else:                               colorPrime = (c, 0, x)

    if len(color) == 4:
        return (
            round((colorPrime[R] + m) * (MAX_COLOR_VALUE - 1), 2),
            round((colorPrime[G] + m) * (MAX_COLOR_VALUE - 1), 2),
            round((colorPrime[B] + m) * (MAX_COLOR_VALUE - 1), 2),
            color[ALPHA])

    return (
        round((colorPrime[R] + m) * (MAX_COLOR_VALUE - 1), 2),
        round((colorPrime[G] + m) * (MAX_COLOR_VALUE - 1), 2),
        round((colorPrime[B] + m) * (MAX_COLOR_VALUE - 1), 2))

def rgb_to_hsl(color, hueInDegrees = True):

    """Converts from RGB to HSL color format."""

    assert type(color) in (tuple, list) and len(color) in (3, 4)
    assert type(hueInDegrees) == bool

    for i in color: assert type(i) in (int, float) and i >= 0 and i <= (MAX_COLOR_VALUE - 1)
    
    colorPrime = (
        color[R] / (MAX_COLOR_VALUE - 1),
        color[G] / (MAX_COLOR_VALUE - 1),
        color[B] / (MAX_COLOR_VALUE - 1))

    cMax = max((colorPrime[R], colorPrime[G], colorPrime[B]))
    cMin = min((colorPrime[R], colorPrime[G], colorPrime[B]))
    delta = cMax - cMin

    l = (cMax + cMin) / 2
    s = 0 if delta == 0 else delta / (1 - abs((2 * l) - 1))
    h = -1

    if delta == 0:
        h = 0
    elif cMax == colorPrime[R]:
        h = 60 * (((colorPrime[G] - colorPrime[B]) / delta) % 6)
    elif cMax == colorPrime[G]:
        h = 60 * (((colorPrime[B] - colorPrime[R]) / delta) + 2)
    else:
        h = 60 * (((colorPrime[R] - colorPrime[G]) / delta) + 4)

    if not hueInDegrees: h /= FULL_ROTATION

    if len(color) == 4:
        return (round(h, 2), round(s, 2), round(l, 2), color[ALPHA])

    return (round(h, 2), round(s, 2), round(l, 2))
