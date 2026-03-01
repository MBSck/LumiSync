"""
Utility modules for the LumiSync GUI.
"""

from ...config.options import GENERAL

if GENERAL.platform == "Windows":

    from .validators import IPAddressValidator, MACAddressValidator, PortValidator
    from .window_effects import (
        apply_qt_translucent_background,
        enable_windows_dwm_blur,
        enable_windows_backdrop,
        WindowsBackdropType,
    )

    __all__ = [
        "IPAddressValidator",
        "MACAddressValidator",
        "PortValidator",
        "apply_qt_translucent_background",
        "enable_windows_dwm_blur",
        "enable_windows_backdrop",
        "WindowsBackdropType",
    ]
