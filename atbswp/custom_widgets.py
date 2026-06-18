"""Custom Widgets created to modify the settings."""

# atbswp: Record mouse and keyboard actions and reproduce them identically at will
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

import wx


class SliderDialog(wx.Dialog):
    """Wrap a slider in a dialog and get the value"""

    def __init__(self, *args, **kwargs):
        """Initialize the widget with the custom attributes."""
        self._current_value = kwargs.pop("default_value", 1)
        self.min_value = kwargs.pop("min_value", 1)
        self.max_value = kwargs.pop("max_value", 999)
        super(SliderDialog, self).__init__(*args, **kwargs)
        self._value = 1
        self.init_ui()
        self.slider.Bind(wx.EVT_KEY_UP, self.on_esc_press)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def init_ui(self):
        """Initialize the UI elements"""
        pnl = wx.Panel(self)
        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.slider = wx.Slider(parent=pnl, id=wx.ID_ANY, value=self._current_value,
                                minValue=self.min_value, maxValue=self.max_value,
                                name="Choose a number", size=self.GetSize(),
                                style=wx.SL_VALUE_LABEL | wx.SL_AUTOTICKS)
        sizer.Add(self.slider)
        pnl.SetSizer(sizer)
        sizer.Fit(self)

    def on_esc_press(self, event):
        """Close the dialog if the user presses ESC"""
        if event.KeyCode == wx.WXK_ESCAPE:
            self.Close()
        event.Skip()

    def on_close(self, event):
        """Triggered when the widget is closed."""
        self._value = self.slider.Value
        self.Destroy()

    @property
    def value(self):
        """Getter."""
        return self._value

    @value.setter
    def value(self, value):
        """Setter."""
        self._value = value


class ReportDialog(wx.Dialog):
    """Show a text report and let the user save it to a file."""

    def __init__(self, parent, title, text):
        super(ReportDialog, self).__init__(
            parent, title=title, size=(560, 420),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self._text = text
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(
            self, value=text,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        # Monospace font so the loop list lines up like a table.
        self.text_ctrl.SetFont(
            wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL))
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 8)

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(self, label="Enregistrer…")
        close_button = wx.Button(self, wx.ID_CLOSE, "Fermer")
        buttons.Add(save_button, 0, wx.RIGHT, 6)
        buttons.Add(close_button, 0)
        sizer.Add(buttons, 0, wx.ALIGN_RIGHT | wx.ALL, 8)

        self.SetSizer(sizer)
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        close_button.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_CLOSE))

    def on_save(self, event):
        """Save the report to a UTF-8 text file."""
        with wx.FileDialog(
                self, "Enregistrer le rapport", defaultFile="rapport.txt",
                wildcard="Fichiers texte (*.txt)|*.txt",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            try:
                with open(file_dialog.GetPath(), "w", encoding="utf-8") as f:
                    f.write(self._text)
            except IOError:
                wx.LogError("Impossible d'enregistrer le rapport.")
