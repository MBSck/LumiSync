import time

import colour
import dxcam
from PIL import Image

from .. import connection, utils

# TODO: Move this out of global space?
ss = dxcam.create()


def start() -> None:
    """Starts the monitor-light synchronisation."""
    connection.switch_razer(True)

    # NOTE: Initialises with black colors
    previous_colors = [(0, 0, 0)] * 10
    while True:
        colors = []
        try:
            screen = ss.grab()
            if screen is None:
                continue

            screen = Image.fromarray(screen)
            width, height = screen.size
        except OSError:
            print("Warning: Screenshot failed, trying again...")
            continue

        top, bottom = int(height / 4 * 2), int(height / 4 * 3)

        for x in range(4):
            img = screen.crop((int(width / 4 * x), 0, int(width / 4 * (x + 1)), top))
            point = (int(img.size[0] / 2), int(img.size[1] / 2))
            colors.append(img.getpixel(point))
        colors.reverse()
        img = screen.crop((0, top, int(width / 4), bottom))
        point = (int(img.size[0] / 2), int(img.size[1] / 2))
        colors.append(img.getpixel(point))
        for x in range(4):
            img = screen.crop(
                (int(width / 4 * x), bottom, int(width / 4 * (x + 1)), height)
            )
            point = (int(img.size[0] / 2), int(img.size[1] / 2))
            colors.append(img.getpixel(point))
        img = screen.crop((int((width / 4 * 3)), top, width, bottom))
        colors.append(img.getpixel(point))

        smooth_transition(previous_colors, colors)
        previous_colors = colors


def smooth_transition(previous_colors, colors, steps: int = 10, delay: float = 0.01) -> None:
    """Computes a smooth transition of the colors and sends it to a device."""
    prev_colors = [
        colour.Color(rgb=(c[0] / 255, c[1] / 255, c[2] / 255)) for c in previous_colors
    ]
    next_colors = [
        colour.Color(rgb=(c[0] / 255, c[1] / 255, c[2] / 255)) for c in colors
    ]

    # TODO: There is probably a quicker way to do this with the numpy package or so -> Check
    for step in range(steps):
        interpolated_colors = []
        for i in range(len(colors)):
            r = utils.lerp(prev_colors[i].red, next_colors[i].red, step / steps)
            g = utils.lerp(prev_colors[i].green, next_colors[i].green, step / steps)
            b = utils.lerp(prev_colors[i].blue, next_colors[i].blue, step / steps)
            interpolated_colors.append((int(r * 255), int(g * 255), int(b * 255)))

        connection.send_razer_data(utils.convert_colors(interpolated_colors))
        time.sleep(delay)
