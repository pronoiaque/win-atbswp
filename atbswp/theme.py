"""Visual theme (colors and logo) borrowed from the winghost-monitor project.

The palette is inspired by the CHU Toulouse branding used in
https://github.com/pronoiaque/winghost-monitor (blue / green / red on a dark
background). Centralising the colors here keeps the GUI consistent and makes it
trivial to re-skin the whole application.
"""

import os
import sys
from pathlib import Path

import wx


# --- Palette (CHU / winghost-monitor) -------------------------------------
BLUE = wx.Colour(0x00, 0x91, 0xCE)      # #0091CE  primary
GREEN = wx.Colour(0x8B, 0xC5, 0x3F)     # #8BC53F  success / replay
RED = wx.Colour(0xD6, 0x45, 0x50)       # #D64550  record / stop
DARK = wx.Colour(0x1E, 0x2A, 0x38)      # #1E2A38  text / background
LIGHT = wx.Colour(0xF4, 0xF8, 0xFB)     # #F4F8FB  panels
AMBER = wx.Colour(0xE8, 0xA3, 0x3D)     # #E8A33D  warning / auto
WHITE = wx.Colour(0xFF, 0xFF, 0xFF)


def asset_path():
    """Return the directory holding the bundled images."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return Path(__file__).parent.absolute()


def logo_bitmap(max_width=180):
    """Load the CHU logo, scaled to fit ``max_width`` while keeping ratio."""
    path = os.path.join(asset_path(), "img", "logo_chu.png")
    image = wx.Image(path, wx.BITMAP_TYPE_ANY)
    w, h = image.GetWidth(), image.GetHeight()
    if w > max_width:
        ratio = max_width / float(w)
        image = image.Scale(max_width, int(h * ratio), wx.IMAGE_QUALITY_HIGH)
    return wx.Bitmap(image)


def app_icon():
    """Application/taskbar icon (the CHU logo)."""
    return wx.Icon(os.path.join(asset_path(), "img", "logo_chu.png"))


def style_button(button, bg, fg=WHITE):
    """Apply a colored, flat look to a (toggle) button."""
    button.SetBackgroundColour(bg)
    button.SetForegroundColour(fg)
