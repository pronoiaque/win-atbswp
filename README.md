# win-atbswp
![Logo](./atbswp/img/logo_chu.png)

**win-atbswp** is a fork of [atbswp](https://github.com/RMPR/atbswp) (Automate
the Boring Stuff with Python) that records your mouse and keyboard actions and
replays them identically as many times as you want.

On top of the original tool, this fork adds three things tailored for
unattended, repeatable monitoring runs:

* **Scenario (session) management** — save several named captures and switch
  between them from a dropdown, instead of juggling a single capture file.
* **Auto-replay (the "Auto" button)** — replay the active scenario
  automatically on a fixed schedule, with a configurable interval
  (**30 minutes by default**).
* **CHU / winghost-monitor look & feel** — the logo and color palette from
  [winghost-monitor](https://github.com/pronoiaque/winghost-monitor).

## New features

### Scenarios (sessions)

A *scenario* is a saved capture stored under your config directory
(`~/.config/atbswp_scenarios` on Linux, `%APPDATA%\atbswp_scenarios` on
Windows), one `.py` file per scenario.

* Use the **Scenario** dropdown to pick the active scenario; its capture is
  loaded as the current working capture.
* **+** creates a new (empty) scenario, **Rename** renames the active one, and
  **X** deletes it.
* Recording, or loading a capture from disk, automatically updates the active
  scenario on disk.

The active scenario is remembered across restarts.

### Auto-replay ("Auto")

Toggle the **Auto** button to replay the active scenario on a schedule. The
first replay fires immediately, then it repeats every *Auto Replay Interval*
seconds (default **1800s = 30 min**). A new replay is skipped if the previous
one is still running.

Change the interval from **Preferences (cog) → Auto Replay Interval**, expressed
in minutes. The auto-replay state and interval are persisted across restarts.

### Theme

The interface uses the CHU Toulouse palette from winghost-monitor:

| Role            | Color     |
|-----------------|-----------|
| Primary (blue)  | `#0091CE` |
| Success (green) | `#8BC53F` |
| Record (red)    | `#D64550` |
| Auto (amber)    | `#E8A33D` |
| Text / dark     | `#1E2A38` |

## Install instructions

### From source

Debian / Ubuntu
```shell
sudo apt install git python3-dev python3-tk python3-setuptools python3-wheel python3-pip python3-wxgtk4.0
git clone https://github.com/pronoiaque/win-atbswp.git && cd win-atbswp
python3 -m pip install pyautogui pynput --user
python3 atbswp/main.py
```

Fedora
```shell
sudo dnf install python3-wxpython4 python3-xlib python3-tkinter
git clone https://github.com/pronoiaque/win-atbswp.git && cd win-atbswp
python3 -m pip install pyautogui pynput --user
python3 atbswp/main.py
```

Windows
```shell
git clone https://github.com/pronoiaque/win-atbswp
cd win-atbswp
pip install wxPython pyautogui pynput
python atbswp\main.py
```

## Credits

* Original project: [atbswp](https://github.com/RMPR/atbswp) by Paul Mairo
  (GNU GPL v3).
* Logo & color palette: [winghost-monitor](https://github.com/pronoiaque/winghost-monitor).

## License

GNU General Public License v3 — see [LICENSE](./LICENSE).

## Known issues
On Linux, this only works with Xorg. Wayland users have to enable Xorg:

```
sudo sed 's/#WaylandEnable=false/WaylandEnable=false/' /etc/gdm/custom.conf -i # on Gnome
```
