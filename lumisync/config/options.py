import os
import platform
from types import SimpleNamespace

# TODO: Should the led option be moved under a different global?
GENERAL = SimpleNamespace(nled=20, platform=platform.system(), compositor=None)
if GENERAL.platform != "Windows":
    if (
        os.environ.get("WAYLAND_DISPLAY")
        or os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
        or "wayland" in os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    ):
        GENERAL.compositor = "wayland"
    else:
        GENERAL.compositor = "x11"

# TODO: Replace the settings.json with this during runtime
# and only use the settings.json on restart?
CONNECTION = SimpleNamespace(
    default=SimpleNamespace(
        multicast="255.255.255.255",
        port=4001,
        listen_port=4002,
        timeout=1,
    ),
    devices=[],
)
# NOTE: Duration (seconds)
AUDIO = SimpleNamespace(sample_rate=48000, duration=0.01)

# TODO: This needs to change as soon as support for multiple devices
# is being implemented -> Similar with next as for the devices query?
COLORS = SimpleNamespace(previous=[], current=[])

# NOTE: Brightness settings for different sync modes (percent)
BRIGHTNESS = SimpleNamespace(monitor=0.75, music=0.85)
