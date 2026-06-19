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

"""
This module contains all the classes needed to
create the GUI and handle non functionnal event
"""

import os
import sys
import time
from pathlib import Path

import control

import settings

import theme

from custom_widgets import ReportDialog

import wx
import wx.adv


# Product identity shown in the title bar and next to the logo.
APP_TITLE = "WinGhost Monitor"
APP_SUBTITLE = "Automatisation & monitoring de scénarios"


class MainDialog(wx.Dialog, wx.MiniFrame):
    """Main Window, a dialog to display the app correctly even on tiling WMs."""

    app_text = ["Load Capture", "Save", "Start/Stop Capture", "Play", "Compile to executable",
                "Preferences", "Help"]
    settings_text = ["Play &Speed: Fast", "&Infinite Playback", "Set &Repeat Count", "Recording &Hotkey",
                     "&Playback Hotkey", "Always on &Top", "&Language", "&About", "&Exit"]

    def on_settings_click(self, event):
        """Triggered when the popup menu is clicked."""
        self.settings_popup()
        event.GetEventObject().PopupMenu(self.settings_popup())
        event.EventObject.Parent.panel.SetFocus()
        event.Skip()

    def settings_popup(self):
        """Build the popup menu."""
        menu = wx.Menu()
        # Replay fast
        ps = menu.Append(wx.ID_ANY, self.settings_text[0])
        self.Bind(wx.EVT_MENU,
                  control.SettingsCtrl.playback_speed,
                  ps)
        ps.Enable(False)

        #  Infinite Playback
        cp = menu.AppendCheckItem(wx.ID_ANY, self.settings_text[1])
        status = settings.CONFIG.getboolean('DEFAULT', 'Infinite Playback')
        cp.Check(status)
        self.Bind(wx.EVT_MENU,
                  control.SettingsCtrl.infinite_playback,
                  cp)

        # Repeat count
        self.Bind(wx.EVT_MENU, self.sc.repeat_count,
                  menu.Append(wx.ID_ANY, self.settings_text[2]))
        menu.AppendSeparator()

        # Recording hotkey
        self.Bind(wx.EVT_MENU,
                  control.SettingsCtrl.recording_hotkey,
                  menu.Append(wx.ID_ANY, self.settings_text[3]))

        # Playback hotkey
        self.Bind(wx.EVT_MENU,
                  control.SettingsCtrl.playback_hotkey,
                  menu.Append(wx.ID_ANY, self.settings_text[4]))
        menu.AppendSeparator()

        # Auto replay interval
        self.Bind(wx.EVT_MENU,
                  control.SettingsCtrl.auto_replay_interval,
                  menu.Append(wx.ID_ANY, "&Intervalle de rejeu automatique"))
        menu.AppendSeparator()

        # Always on top
        aot = menu.AppendCheckItem(wx.ID_ANY, self.settings_text[5])
        status = settings.CONFIG.getboolean('DEFAULT', 'Always On Top')
        aot.Check(status)
        self.Bind(wx.EVT_MENU,
                  self.sc.always_on_top,
                  aot)

        # Language
        submenu = wx.Menu()
        # Workaround for users of the previous version
        current_lang = "en"
        try:
            current_lang = settings.CONFIG.get('DEFAULT', 'Language')
        except:
            pass

        for language in os.listdir(os.path.join(self.path, "lang")):
            lang_item = submenu.AppendRadioItem(wx.ID_ANY, language)
            self.Bind(wx.EVT_MENU,
                      self.sc.language,
                      lang_item)
            if language == current_lang:
                lang_item.Check(True)
        menu.AppendSubMenu(submenu, self.settings_text[6])

        # About
        self.Bind(wx.EVT_MENU,
                  self.on_about,
                  menu.Append(wx.ID_ABOUT, self.settings_text[7]))

        # Recording Timer
        self.Bind(wx.EVT_MENU,
                  control.RecordCtrl.recording_timer,
                  menu.Append(wx.ID_ANY, self.settings_text[8]))

        # Mouse speed
        self.Bind(wx.EVT_MENU,
                  control.RecordCtrl.mouse_speed,
                  menu.Append(wx.ID_ANY, self.settings_text[9]))
        return menu

    def __init__(self, *args, **kwds):
        """Build the interface."""
        if getattr(sys, 'frozen', False):
            self.path = sys._MEIPASS
        else:
            self.path = Path(__file__).parent.absolute()
        on_top = wx.DEFAULT_DIALOG_STYLE
        on_top = on_top if not settings.CONFIG.getboolean('DEFAULT', 'Always On Top') \
            else on_top | wx.STAY_ON_TOP
        kwds["style"] = kwds.get("style", 0) | on_top
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self)
        # Timestamp of the last Escape key press (for the double-Esc stop).
        self._last_esc = 0.0
        self.icon = theme.app_icon()
        self.SetIcon(self.icon)
        self.taskbar = TaskBarIcon(self)
        self.taskbar.SetIcon(self.icon, APP_TITLE)

        # CHU / winghost-monitor look & feel.
        self.SetBackgroundColour(theme.LIGHT)

        locale = self.__load_locale()
        self.app_text, self.settings_text = locale[:7], locale[7:]

        # --- Header (logo + product name) ------------------------------
        self.logo = wx.StaticBitmap(self, wx.ID_ANY, theme.logo_bitmap())
        self.title = wx.StaticText(self, label=APP_TITLE)
        self.title.SetForegroundColour(theme.DARK)
        title_font = self.title.GetFont()
        title_font.SetPointSize(title_font.GetPointSize() + 4)
        title_font = title_font.Bold()
        self.title.SetFont(title_font)
        self.subtitle = wx.StaticText(self, label=APP_SUBTITLE)
        self.subtitle.SetForegroundColour(theme.BLUE)

        # --- Scenario (session) selector -------------------------------
        self.scc = control.ScenarioCtrl(self)
        self.scenario_label = wx.StaticText(self, label="Scénario :")
        self.scenario_label.SetForegroundColour(theme.DARK)
        self.scenario_choice = wx.ComboBox(self, style=wx.CB_READONLY)
        self.scenario_new_button = wx.Button(self, label="Nouveau")
        self.scenario_new_button.SetToolTip("Nouveau scénario")
        theme.style_button(self.scenario_new_button, theme.GREEN, theme.DARK)
        self.scenario_rename_button = wx.Button(self, label="Renommer")
        self.scenario_rename_button.SetToolTip("Renommer le scénario")
        theme.style_button(self.scenario_rename_button, theme.BLUE)
        self.scenario_delete_button = wx.Button(self, label="Supprimer…")
        self.scenario_delete_button.SetToolTip("Supprimer le scénario")
        theme.style_button(self.scenario_delete_button, theme.RED)

        # --- Action buttons --------------------------------------------
        self.file_open_button = wx.BitmapButton(self,
                                                wx.ID_ANY,
                                                wx.Bitmap(os.path.join(self.path, "img", "file-upload.png"),
                                                          wx.BITMAP_TYPE_ANY))
        self.file_open_button.SetToolTip(self.app_text[0])
        self.save_button = wx.BitmapButton(self,
                                           wx.ID_ANY,
                                           wx.Bitmap(os.path.join(self.path, "img", "save.png"),
                                                     wx.BITMAP_TYPE_ANY))
        self.save_button.SetToolTip(self.app_text[1])
        self.record_button = wx.BitmapToggleButton(self,
                                                   wx.ID_ANY,
                                                   wx.Bitmap(os.path.join(self.path, "img", "video.png"),
                                                             wx.BITMAP_TYPE_ANY))
        self.record_button.SetToolTip(self.app_text[2])
        theme.style_button(self.record_button, theme.RED)
        self.stop_button = wx.BitmapButton(
            self, wx.ID_ANY,
            wx.Bitmap(os.path.join(self.path, "img", "stop.png"),
                      wx.BITMAP_TYPE_ANY))
        theme.style_button(self.stop_button, theme.DARK, theme.WHITE)
        self.stop_button.SetToolTip(
            "Tout arrêter : enregistrement et rejeu automatique "
            "(ou double appui sur Échap)")
        self.play_button = wx.BitmapToggleButton(self,
                                                 wx.ID_ANY,
                                                 wx.Bitmap(os.path.join(self.path, "img", "play-circle.png"),
                                                           wx.BITMAP_TYPE_ANY))
        theme.style_button(self.play_button, theme.GREEN)
        self.remaining_plays = wx.StaticText(self, label=settings.CONFIG.get("DEFAULT", "Repeat Count"),
                                             style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.play_button.SetToolTip(self.app_text[3])

        # --- Auto replay toggle + response-time monitoring -------------
        self.monitor = control.MonitorCtrl()
        self.arc = control.AutoReplayCtrl(self)
        self.auto_button = wx.BitmapToggleButton(
            self, wx.ID_ANY,
            wx.Bitmap(os.path.join(self.path, "img", "auto.png"),
                      wx.BITMAP_TYPE_ANY))
        theme.style_button(self.auto_button, theme.AMBER, theme.DARK)
        self.auto_button.SetToolTip("Rejeu automatique à intervalle régulier")
        self.auto_status = wx.StaticText(self, label="")
        self.auto_status.SetForegroundColour(theme.DARK)
        self.report_button = wx.BitmapButton(
            self, wx.ID_ANY,
            wx.Bitmap(os.path.join(self.path, "img", "report.png"),
                      wx.BITMAP_TYPE_ANY))
        theme.style_button(self.report_button, theme.BLUE)
        self.report_button.SetToolTip("Rapport de temps de réponse")

        self.settings_button = wx.BitmapButton(self,
                                               wx.ID_ANY,
                                               wx.Bitmap(os.path.join(self.path, "img", "cog.png"),
                                                         wx.BITMAP_TYPE_ANY))
        self.settings_button.SetToolTip(self.app_text[5])

        self.__add_bindings()
        self.__set_properties()
        self.__do_layout()
        self.refresh_scenarios()
        self.__restore_auto_replay()

    def __load_locale(self):
        """Load the interface in user-defined language (default english)."""
        try:
            lang = settings.CONFIG.get('DEFAULT', 'Language')
            # Read as UTF-8 so accented characters render correctly on Windows
            # (the default cp1252 codec would garble them, e.g. in the menu).
            locale = open(os.path.join(self.path, "lang", lang),
                          encoding="utf-8").read().splitlines()
        except:
            return self.app_text + self.settings_text

        return locale

    def __add_bindings(self):
        # file_save_ctrl
        self.fsc = control.FileChooserCtrl(self)
        self.Bind(wx.EVT_BUTTON, self.fsc.load_file, self.file_open_button)
        self.Bind(wx.EVT_BUTTON, self.fsc.save_file, self.save_button)

        # record_button_ctrl
        self.rbc = control.RecordCtrl()
        self.Bind(wx.EVT_TOGGLEBUTTON, self.rbc.action, self.record_button)

        # stop_button_ctrl (stops recording and auto-replay)
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.stop_button)

        # play_button_ctrl
        self.pbc = control.PlayCtrl()
        self.Bind(wx.EVT_TOGGLEBUTTON, self.pbc.action, self.play_button)

        # Handle the event returned after a playback has completed
        self.Bind(self.pbc.EVT_THREAD_END, self.on_thread_end)

        # Scenario management
        self.Bind(wx.EVT_COMBOBOX, self.on_scenario_select, self.scenario_choice)
        self.Bind(wx.EVT_BUTTON, self.on_scenario_new, self.scenario_new_button)
        self.Bind(wx.EVT_BUTTON, self.on_scenario_rename, self.scenario_rename_button)
        self.Bind(wx.EVT_BUTTON, self.on_scenario_delete, self.scenario_delete_button)

        # Auto replay
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_auto_toggle, self.auto_button)

        # Response-time report
        self.Bind(wx.EVT_BUTTON, self.on_report, self.report_button)

        # settings_button_ctrl
        self.Bind(wx.EVT_BUTTON, self.on_settings_click, self.settings_button)
        self.sc = control.SettingsCtrl(self)

        self.Bind(wx.EVT_CLOSE, self.on_close_dialog)

        # Handle keyboard shortcuts
        self.panel.Bind(wx.EVT_KEY_UP, self.on_key_press)

        self.panel.SetFocus()

    def __set_properties(self):
        self.file_open_button.SetSize(self.file_open_button.GetBestSize())
        self.save_button.SetSize(self.save_button.GetBestSize())
        self.record_button.SetSize(self.record_button.GetBestSize())
        self.stop_button.SetSize(self.stop_button.GetBestSize())
        self.play_button.SetSize(self.play_button.GetBestSize())
        self.auto_button.SetSize(self.auto_button.GetBestSize())
        self.report_button.SetSize(self.report_button.GetBestSize())
        self.settings_button.SetSize(self.settings_button.GetBestSize())

    def __do_layout(self):
        self.remaining_plays.SetBackgroundColour(theme.DARK)
        self.remaining_plays.SetForegroundColour(theme.WHITE)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Header: logo + product name (title over subtitle)
        title_sizer = wx.BoxSizer(wx.VERTICAL)
        title_sizer.Add(self.title, 0, wx.ALIGN_LEFT)
        title_sizer.Add(self.subtitle, 0, wx.ALIGN_LEFT | wx.TOP, 2)
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        header_sizer.Add(self.logo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 6)
        header_sizer.Add(title_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 6)
        main_sizer.Add(header_sizer, 0, wx.EXPAND)

        # Scenario selector row
        scenario_sizer = wx.BoxSizer(wx.HORIZONTAL)
        scenario_sizer.Add(self.scenario_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
        scenario_sizer.Add(self.scenario_choice, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
        scenario_sizer.Add(self.scenario_new_button, 0, wx.ALL, 2)
        scenario_sizer.Add(self.scenario_rename_button, 0, wx.ALL, 2)
        scenario_sizer.Add(self.scenario_delete_button, 0, wx.ALL, 2)
        main_sizer.Add(scenario_sizer, 0, wx.EXPAND)

        # Action buttons row
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.panel, 0, 0, 0)
        buttons_sizer.Add(self.file_open_button, 0, 0, 0)
        buttons_sizer.Add(self.save_button, 0, 0, 0)
        buttons_sizer.Add(self.record_button, 0, 0, 0)
        buttons_sizer.Add(self.stop_button, 0, 0, 0)
        buttons_sizer.Add(self.play_button, 0, 0, 0)
        buttons_sizer.Add(self.auto_button, 0, 0, 0)
        buttons_sizer.Add(self.report_button, 0, 0, 0)
        buttons_sizer.Add(self.settings_button, 0, 0, 0)
        main_sizer.Add(buttons_sizer, 0, wx.EXPAND)

        # Status row
        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        status_sizer.Add(self.remaining_plays, 0, wx.ALL, 4)
        status_sizer.Add(self.auto_status, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 8)
        main_sizer.Add(status_sizer, 0, wx.EXPAND)

        self.SetSizer(main_sizer)
        self.Centre()
        main_sizer.Fit(self)
        self.Layout()

    # ---------------------------------------------------------------
    # Scenario (session) management
    # ---------------------------------------------------------------
    def refresh_scenarios(self):
        """Refresh the scenario combobox from disk and reflect the active one."""
        names = self.scc.list_scenarios()
        self.scenario_choice.Set(names)
        current = self.scc.current
        if current and current in names:
            self.scenario_choice.SetStringSelection(current)
        else:
            self.scenario_choice.SetSelection(wx.NOT_FOUND)
        has_selection = bool(current) and current in names
        self.scenario_rename_button.Enable(has_selection)
        self.scenario_delete_button.Enable(has_selection)

    def on_scenario_select(self, event):
        """Load the scenario chosen by the user."""
        name = self.scenario_choice.GetStringSelection()
        if name:
            self.scc.load(name)
        self.refresh_scenarios()
        self.panel.SetFocus()

    def on_scenario_new(self, event):
        """Prompt for a name and create a new (empty) scenario."""
        dlg = wx.TextEntryDialog(self, "Nom du nouveau scénario :",
                                 "Nouveau scénario")
        if dlg.ShowModal() == wx.ID_OK:
            if self.scc.create(dlg.GetValue()):
                self.refresh_scenarios()
        dlg.Destroy()
        self.panel.SetFocus()

    def on_scenario_rename(self, event):
        """Rename the active scenario."""
        current = self.scc.current
        if not current:
            return
        dlg = wx.TextEntryDialog(self, "Nouveau nom :", "Renommer le scénario",
                                 current)
        if dlg.ShowModal() == wx.ID_OK:
            if self.scc.rename(current, dlg.GetValue()):
                self.refresh_scenarios()
        dlg.Destroy()
        self.panel.SetFocus()

    def on_scenario_delete(self, event):
        """Delete the active scenario after confirmation."""
        current = self.scc.current
        if not current:
            return
        dlg = wx.MessageDialog(self,
                               message=f"Supprimer le scénario « {current} » ?",
                               caption="Confirmer la suppression",
                               style=wx.YES_NO | wx.ICON_WARNING)
        if dlg.ShowModal() == wx.ID_YES:
            self.scc.delete(current)
            self.refresh_scenarios()
        dlg.Destroy()
        self.panel.SetFocus()

    # ---------------------------------------------------------------
    # Auto replay
    # ---------------------------------------------------------------
    def __restore_auto_replay(self):
        """Resume auto-replay if it was enabled in a previous session."""
        try:
            enabled = settings.CONFIG.getboolean('DEFAULT', 'Auto Replay')
        except (ValueError, KeyError):
            enabled = False
        if enabled:
            self.auto_button.SetValue(True)
            self.arc.start()
        self.__update_auto_status()

    def on_auto_toggle(self, event):
        """Enable or disable scheduled auto-replay."""
        if self.auto_button.GetValue():
            self.arc.start()
        else:
            self.arc.stop()
        self.__update_auto_status()
        self.panel.SetFocus()

    def __update_auto_status(self):
        if self.arc.is_running():
            minutes = max(1, round(self.arc.interval_seconds() / 60))
            self.auto_status.SetLabel(f"Rejeu automatique toutes les {minutes} min")
        else:
            self.auto_status.SetLabel("")
        self.Layout()

    def on_key_press(self, event):
        """ Create manually the event when the correct key is pressed."""
        keycode = event.GetKeyCode()

        if keycode == wx.WXK_F1:
            control.HelpCtrl.action(wx.PyCommandEvent(wx.wxEVT_BUTTON))

        elif keycode == settings.CONFIG.getint('DEFAULT', 'Recording Hotkey'):
            btn_event = wx.CommandEvent(wx.wxEVT_TOGGLEBUTTON)
            btn_event.EventObject = self.record_button
            if not self.record_button.Value:
                self.record_button.Value = True
                self.rbc.action(btn_event)
            else:
                self.record_button.Value = False
                self.rbc.action(btn_event)

        elif keycode == settings.CONFIG.getint('DEFAULT', 'Playback Hotkey'):
            if not self.play_button.Value:
                self.play_button.Value = True
                btn_event = wx.CommandEvent(wx.wxEVT_TOGGLEBUTTON)
                btn_event.EventObject = self.play_button
                self.pbc.action(btn_event)
            else:
                self.play_button.Value = False

        elif keycode == ord("R") and event.CmdDown():
            menu_event = wx.CommandEvent(wx.wxEVT_MENU)
            self.sc.repeat_count(menu_event)

        elif keycode == ord("O") and event.CmdDown():
            btn_event = wx.CommandEvent(wx.wxEVT_TOGGLEBUTTON)
            btn_event.EventObject = self.file_open_button
            self.fsc.load_file(btn_event)

        elif keycode == ord("S") and event.CmdDown():
            btn_event = wx.CommandEvent(wx.wxEVT_TOGGLEBUTTON)
            btn_event.EventObject = self.save_button
            self.fsc.save_file(btn_event)

        elif keycode == wx.WXK_ESCAPE:
            # Two Escape presses within a second stop everything.
            now = time.monotonic()
            if now - self._last_esc <= 1.0:
                self._last_esc = 0.0
                self.stop_all()
            else:
                self._last_esc = now

        event.Skip()

    def on_thread_end(self, event):
        self.play_button.Value = event.toggle_value
        self.remaining_plays.Label = str(event.count) if event.count > 0 else \
            str(settings.CONFIG.getint('DEFAULT', 'Repeat Count'))
        self.remaining_plays.Update()
        # The replay is fully finished (input response validated): stop the
        # chrono for this monitoring loop.
        if not event.toggle_value:
            self.monitor.end_loop()

    def on_report(self, event):
        """Display (and optionally save) the response-time report."""
        dlg = ReportDialog(self, "Rapport de temps de réponse",
                           self.monitor.report_text())
        dlg.ShowModal()
        dlg.Destroy()
        self.panel.SetFocus()

    # ---------------------------------------------------------------
    # Stop everything (button + double-Escape)
    # ---------------------------------------------------------------
    def on_stop(self, event):
        """Handler for the STOP button."""
        self.stop_all()
        self.panel.SetFocus()

    def stop_all(self):
        """Stop recording, auto-replay and any replay in progress."""
        # Stop an ongoing recording.
        if self.record_button.Value:
            self.record_button.Value = False
            btn_event = wx.CommandEvent(wx.wxEVT_TOGGLEBUTTON)
            btn_event.EventObject = self.record_button
            self.rbc.action(btn_event)
        # Stop scheduled auto-replay.
        if self.arc.is_running():
            self.arc.stop()
            self.auto_button.SetValue(False)
            self.__update_auto_status()
        # Stop a replay currently running.
        if self.play_button.Value:
            self.play_button.Value = False
            btn_event = wx.CommandEvent(wx.wxEVT_TOGGLEBUTTON)
            btn_event.EventObject = self.play_button
            self.pbc.action(btn_event)

    def on_exit_app(self, event):
        """Clean exit saving the settings."""
        self.arc.stop()
        settings.save_config()
        self.Destroy()
        self.taskbar.Destroy()

    def on_close_dialog(self, event):
        """Confirm exit."""
        dialog = wx.MessageDialog(self,
                                  message="Voulez-vous vraiment quitter ?",
                                  caption="Confirmer la fermeture",
                                  style=wx.YES_NO,
                                  pos=wx.DefaultPosition)
        response = dialog.ShowModal()

        if (response == wx.ID_YES):
            self.on_exit_app(event)
        else:
            event.StopPropagation()

    def on_about(self, event):
        """About dialog."""
        info = wx.adv.AboutDialogInfo()
        info.Name = APP_TITLE
        info.Version = f"{settings.VERSION}"
        info.Copyright = (f"©{settings.YEAR} Paul Mairo <github@rmpr.xyz>\n")
        info.Description = (
            "Enregistre les actions souris/clavier et les rejoue à l'identique.\n"
            "Gestion de scénarios, rejeu automatique et monitoring du temps de "
            "réponse.\nThème CHU inspiré du projet winghost-monitor ; "
            "fork de atbswp (Paul Mairo).")
        info.WebSite = ("https://github.com/pronoiaque/win-atbswp",
                        "Page du projet")
        info.Developers = ["Paul Mairo (atbswp)"]
        info.License = "GNU General Public License V3"
        info.Icon = self.icon
        wx.adv.AboutBox(info)


class TaskBarIcon(wx.adv.TaskBarIcon):
    """Taskbar showing the state of the recording."""

    def __init__(self, parent):
        self.parent = parent
        super(TaskBarIcon, self).__init__()
