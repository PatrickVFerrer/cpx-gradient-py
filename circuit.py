from adafruit_circuitplayground.express import cpx

from random import randint
import colorsys
# from random import randbool
# randbool doesn't import for w/e reason . . .

step_index = 0
speed_index = 0

def scale(n, start1, stop1, start2, stop2):
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2

def hls_to_rgb(tupl):
    tupl = colorsys.hls_to_rgb(*tupl)
    tupl = list(tupl)
    for i in range(3):
        tupl[i] = scale(tupl[i], 0, 1, 0, 255)
        tupl[i] = int(round(tupl[i]))
        if tupl[i] > 255:
            tupl[i] = 255
        if tupl[i] < 0:
            tupl[i] = 0
    return tuple(tupl)

def rgb_to_hls(tupl):
    tupl = list(tupl)
    for i in range(3):
        tupl[i] = scale(tupl[i], 0, 255, 0, 1)
    return colorsys.rgb_to_hls(*tupl)

def gradient(tupl, speed):
    tupl = rgb_to_hls(tupl)
    tupl = list(tupl)

    tupl[0] = scale(tupl[0], 0, 1, 0, 360)
    tupl[0] = (tupl[0] + speed) % 360
    tupl[0] = scale(tupl[0], 0, 360, 0, 1)

    return hls_to_rgb(tupl)

def change_mode():
    global speed_index
    global step_index
    global speeds
    if cpx.button_a and cpx.button_b:
        speeds = list(map(lambda x: x * -1, speeds))
    if cpx.switch:
        if cpx.button_b:
            speed_index = (speed_index - 1) % len(speeds)
        if cpx.button_a:
            speed_index = (speed_index + 1) % len(speeds)
    else:
        if cpx.button_b:
            step_index = (step_index - 1) % len(steps)
        if cpx.button_a:
            step_index = (step_index + 1) % len(steps)

cpx.pixels.brightness = .9

# Color wheel
theta = randint(0, 360)
colors = [
    hls_to_rgb((
        scale(theta, 0, 360, 0, 1),
        randint(45, 60) / 100.0,
        randint(70, 100) / 100.0
    ))
]
default_colors = colors.copy()

steps = [360, 180, 72, 36]
speeds = [360, 9, 18, 36, 72]

for i in range(9):
    next = gradient(colors[i], steps[step_index])
    colors.append(next)

# Step = # of degrees between each
# consecutive LED color on HSL color wheel
#
# 360 divided by Step = # of unique
# colors displayed & repeating across board

cpx.pixels.show()
while True:
    change_mode()
    step = steps[step_index]
    speed = speeds[speed_index]
    if (not cpx.switch) and (cpx.button_a or cpx.button_b):
        colors = default_colors.copy()
        for i in range(9):
            next = gradient(colors[i], step)
            colors.append(next)
    for i in range(10):
        colors[i] = gradient(colors[i], speed)
        cpx.pixels[i] = colors[i]
    print(f"""======================================
# of unique colors: {360 / step}
Circle speed (in LEDs per cycle): {(speed / 36) % 10}
======================================""")

""" All lights have same gradient
theta = randint(0, 360)
tupl = hls_to_rgb((
    scale(theta, 0, 360, 0, 1),
    randint(45, 60) / 100.0,
    randint(70, 100) / 100.0
))

cpx.pixels.show()
while True:
    tupl = gradient(tupl, 1)
    cpx.pixels.fill(tupl)
"""

""" R-G-B Gradient

cpx.pixels.brightness = 0.3
cpx.pixels.fill((0, 0, 0))

tupl = (0, 0, 0)

cpx.pixels.show()
while True:
    tupl = gradient(tupl)
    cpx.pixels.fill(tupl)
"""

""" Circling Rainbow

import time

leds = [
        (255, 0, 0),
        (255, 127, 0),
        (0, 255, 0),
        (0, 255, 127),
        (75, 0, 130),
        (60, 0, 255),
        (255, 255, 255),
        (0, 100, 0),
        (100, 0, 0),
        (0, 0, 100)
    ]

cpx.pixels.brightness = 0.3
cpx.pixels.fill((0, 0, 0))

while True:
    for i in range(10):
        time.sleep(0.1)
        cpx.pixels[i] = leds[i]
        cpx.pixels.show()
        cpx.pixels[i] = (0, 0, 0)
"""

"""
cpx.pixels.fill((0, 150, 255))
while True:
    cpx.pixels.show()
"""

"""
def randbool():
    n = randint(0, 1)
    if n == 0:
        return False
    else:
        return True
"""