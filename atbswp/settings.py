#!/usr/bin/env python3
# Record mouse and keyboard actions and reproduce them identically at will
#
# Copyright (C) 2019 Paul Mairo <github@rmpr.xyz>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Handle the config file of the program

import configparser
import os
import platform
from datetime import date


CONFIG = configparser.ConfigParser()
VERSION = "0.4.1"
YEAR = date.today().strftime("%Y")


# Default values used both to bootstrap a fresh config file and to backfill
# keys that are missing when the user upgrades from a previous version.
DEFAULTS = {
    "Fast Play Speed": "False",
    "Infinite Playback": "False",
    "Repeat Count": "1",
    "Recording Hotkey": "348",
    "Playback Hotkey": "349",
    "Always On Top": "True",
    "Language": "en",
    "Recording Timer": "0",
    "Mouse Speed": "21",
    # Name of the currently active scenario (session). Empty means none.
    "Current Scenario": "",
    # Auto-replay: replay the active capture on a fixed schedule.
    "Auto Replay": "False",
    # Interval between two automatic replays, in seconds (default: 30 minutes).
    "Auto Replay Interval": "1800",
}


# Folder where the named scenarios (sessions) are stored, one .py capture each.
SCENARIOS_DIRNAME = "atbswp_scenarios"


# Check the location of the configuration file, default to the home directory
filename = "atbswp.cfg"
if platform.system() == "Linux":
    config_dir = os.path.join(os.environ.get("HOME") or os.path.expanduser("~"),
                              ".config")
elif platform.system() == "Windows":
    # %APPDATA% is the canonical per-user config location on Windows; fall back
    # to the home directory in the rare case it is not defined.
    config_dir = os.environ.get("APPDATA") or os.path.expanduser("~")
else:
    config_dir = os.environ.get("HOME") or os.path.expanduser("~")

config_location = os.path.join(config_dir, filename)

# Scenarios live next to the configuration file.
SCENARIOS_DIR = os.path.join(config_dir, SCENARIOS_DIRNAME)


def save_config():
    with open(config_location, "w") as config_file:
        CONFIG.write(config_file)


def _ensure_defaults():
    """Make sure every expected key exists (handles config upgrades)."""
    for key, value in DEFAULTS.items():
        if not CONFIG.has_option("DEFAULT", key):
            CONFIG["DEFAULT"][key] = value


try:
    with open(config_location) as config_file:
        CONFIG.read(config_location)
except:
    CONFIG["DEFAULT"] = dict(DEFAULTS)

_ensure_defaults()

# Make sure the scenarios folder exists.
try:
    os.makedirs(SCENARIOS_DIR, exist_ok=True)
except OSError:
    pass
